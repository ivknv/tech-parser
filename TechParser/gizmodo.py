#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser import parser

def get_articles():
	parsed = feedparser.parse('http://gizmodo.com/rss')
	return [{'title': article['title'],
		'link': article['link'],
		'summary': parser.clean_text(article['summary']),
		'source': 'gizmodo'} for article in parsed['entries']]
