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
        
        score = classifier.classify_article(article)['interesting']
        
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
