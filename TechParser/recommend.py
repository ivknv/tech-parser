#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import copy
from collections import Counter

from TechParser import get_conf, save
from TechParser.py2x import *
from TechParser.db_functions import *

if get_conf.config is None:
    get_conf.set_config_auto()

r0 = re.compile(r"<.*?>", re.UNICODE)
r1 = re.compile(r"(?P<g1>\w+)n['\u2019]t", re.UNICODE)
r2 = re.compile(r"(?P<g1>\w+)['\u2019]s", re.UNICODE)
r3 = re.compile(r"(?P<g1>\w+)['\u2019]m", re.UNICODE)
r4 = re.compile(r"(?P<g1>\w+)['\u2019]re", re.UNICODE)
r5 = re.compile(r"(?P<g1>\w+)['\u2019]ve", re.UNICODE)
r6 = re.compile(r"(?P<g1>\w+)['\u2019]d", re.UNICODE)
r7 = re.compile(r"(?P<g1>\w+)['\u2019]ll", re.UNICODE)
r8 = re.compile(r"\bgonna\b", re.UNICODE)
r9 = re.compile(r"\W", re.UNICODE)
r10 = re.compile(r"&#?\w+;", re.UNICODE)

class Pairs(object):
    def __init__(self, text):
        self.pairs = pairs_fromstring(text)
        self.length = sum(dict_values(self.pairs))
    
    def copy(self):
        new = copy.copy(self)
        new.pairs = new.pairs.copy()
        
        return new
    
    def __add__(self, pairs):
        new_pairs = self.copy()
        new_pairs.pairs += pairs.pairs
        new_pairs.length += pairs.length
        
        return new_pairs
    
    def __repr__(self):
        return '<Pairs length={0}>'.format(self.length)

class ArticlePairs(object):
    def __init__(self, title, summary):
        self.title_pairs = Pairs(title)
        self.summary_pairs = Pairs(summary)
        self.all_pairs = self.title_pairs + self.summary_pairs
        self.length = self.all_pairs.length
        self.priority = 1.0

def unescape(text):
    try:
        text = unicode_(text)
    except TypeError:
        pass
    
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text
    
    return r10.sub(fixup, text)

def get_similarity(pairs1, pairs2):
    len_all_pairs = pairs1.length + pairs2.length
    
    if len_all_pairs == 0:
        return 0.0
    
    len_shrd = 0
    for i in find_shared(dict_keys(pairs1.pairs), dict_keys(pairs2.pairs)):
        len_shrd += min(pairs1.pairs[i], pairs2.pairs[i])
    
    return 2.0 * len_shrd / len_all_pairs

def get_similarity2(pairs1, pairs2, force=False):
    if not force:
        try:
            ratio = pairs1.summary_pairs.length / pairs2.summary_pairs.length
        except ZeroDivisionError:
            ratio = 0.0
        
        if ratio > 2.0 or ratio < 0.5 or pairs1.summary_pairs.length < 80 or pairs2.summary_pairs.length < 80:
            return get_similarity(pairs1.title_pairs, pairs2.title_pairs)
    
    
    return get_similarity(pairs1.all_pairs, pairs2.all_pairs)

def pairs_fromstring(s):
    return get_pairs(prepare_string(s))

def article_pairs(a):
    return pairs_fromstring(a['title']), pairs_fromstring(a['summary'])

def get_word_pairs(words):
    pairs = []
    
    for i in words:
        if isinstance(i, list) or isinstance(i, tuple):
            word = i[0]
            priority = 0.0 + i[1] # A faster way to cast to float
        else:
            word = i
            priority = 1.0
        
        p = ArticlePairs(word, '')
        p.priority = priority
        pairs.append(p)
    
    return pairs

def find_similiar(articles):
    interesting_articles = get_interesting_articles()
    blacklist = get_blacklist()
    
    interesting_word_pairs = get_word_pairs(get_conf.config.interesting_words)
    boring_word_pairs = get_word_pairs(get_conf.config.boring_words)
    
    ignored_links = {i['link'] for i in blacklist}
    processed, scores = [], []
    ignored_links.update({i['link'] for i in interesting_articles})
    
    interesting_pairs = [ArticlePairs(i['title'], i['summary']) for i in interesting_articles[:150]]
    ignored_pairs = [ArticlePairs(i['title'], i['summary']) for i in blacklist[:150]]
    empty_pairs = ArticlePairs('', '')
    
    zipped = list(zip_longest(interesting_pairs, ignored_pairs,
        interesting_word_pairs, boring_word_pairs, fillvalue=empty_pairs))
    
    for article in articles:
        if article['link'] in ignored_links or article in processed:
            continue
        
        score = 0.0
        
        pairs1 = ArticlePairs(article['title'], article['summary'])
        
        for (pairs2, pairs3, pairs4, pairs5) in zipped:
            if pairs2.length:
                score += get_similarity2(pairs1, pairs2)
            if pairs3.length:
                score -= get_similarity2(pairs1, pairs3)
            if pairs4.length:
                score += get_similarity(pairs1.all_pairs, pairs4.all_pairs) * pairs4.priority
            if pairs5.length:
                score -= get_similarity(pairs1.all_pairs, pairs5.all_pairs) * pairs5.priority
        
        processed.append(article)
        scores.append(score)
    
    return [[a, s] for (a, s) in zip(processed, scores)]

def prepare_string(s, exclude=["a", "an", "the", "is", "am", "there", "this",
        "are", "for", "that", "of", "to", "so", "in", "on", "off", "those",
        "these", "you", "he", "she", "they", "we", "out"]):
    s = unescape(s.strip().lower())
    s = r0.sub("", s)
    s = r1.sub("\g<g1> not", s)
    s = r2.sub("\g<g1>", s)
    s = r3.sub("\g<g1> am", s)
    s = r4.sub("\g<g1> are", s)
    s = r5.sub("\g<g1> have", s)
    s = r6.sub("\g<g1> would", s)
    s = r7.sub("\g<g1> will", s)
    s = r8.sub("going to", s)
    words = r9.split(s)
    
    return [word for word in words if len(word) and word not in exclude]

def get_pairs(words):
    pairs = Counter()
    for word in words:
        for i in range(len(word)):
            pair = word[i:i+2]
            pairs[pair] += 1
    return pairs

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
        save.dump_somewhere(articles, path)
    except KeyError:
        print('KeyError({0})'.format(addr))
