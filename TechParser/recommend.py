#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from collections import Counter

from TechParser import get_conf, save
from TechParser.py2x import *
from TechParser.db_functions import *
from TechParser.classifier import TextClassifier

if get_conf.config is None:
    get_conf.set_config_auto()

TextClassifier.load_irregular_words()

def findNearestNumber(n, numbers):
    nearest = numbers[0]
    min_distance = abs(n - nearest)
    for i in numbers[1:]:
        d = abs(n - i)
        if d < min_distance:
            min_distance, nearest = d, i
    
    return nearest

def rankByWordCount(num_words):
    n = findNearestNumber(num_words, get_conf.config.perfect_word_count)
    return 1.0 - abs(num_words - n) / (num_words + n)

def rank_articles(articles):
    processed, scores = [], []
    
    classifier = loadClassifier()
    
    for i in get_conf.config.interesting_words:
        if type(i) in {list, tuple, set}:
            word, priority = i
        else:
            priority = 1.0
            word = i
        
        words = TextClassifier.prepare_words(word)
        
        for word in words:
            classifier.counts['interesting'][word] += priority

    for i in get_conf.config.boring_words:
        if type(i) in {list, tuple, set}:
            word, priority = i
        else:
            priority = 1.0
            word = i
        
        words = TextClassifier.prepare_words(word)
        
        for word in words:
            classifier.counts['boring'][word] += priority
    
    for article in articles:
        if article in processed:
            continue
        
        article_text = article['title'] + ' ' + article['summary']
        article_text = classifier.unescape(article_text)
        article_text = classifier.remove_tags(article_text).lower()
        words = classifier.tokenize(article_text)
        words = Counter(classifier.tokenize(classifier.apply_regexes(article_text)))
        del article_text
        
        score = classifier.classify_features(words)['interesting']
        if get_conf.config.perfect_word_count:
            num_words = len(words)
            score = (score + rankByWordCount(num_words)) / 2
        
        processed.append(article)
        scores.append(score)
    
    return [[a, s] for (a, s) in zip(processed, scores)]

def add_article(addr):
    path = os.path.join(get_conf.logdir, 'articles_dumped')
    
    try:
        articles = save.load_from_somewhere(path)
    except IOError:
        log('WARNING: articles_dumped is missing!')
        return
    
    try:
        add_to_interesting(articles[addr])
    except KeyError:
        print('KeyError({0})'.format(addr))

def add_article_to_blacklist(addr):
    path = os.path.join(get_conf.logdir, 'articles_dumped')
    
    try:
        articles = save.load_from_somewhere(path)
    except IOError:
        log('WARNING: articles_dumped is missing!')
        return
    
    try:
        article = articles[addr]
        add_to_blacklist(article)
    except KeyError:
        print('KeyError({0})'.format(addr))
