#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser import parser

def get_articles(collections=[]):
	articles = []
	titles = []
	
	if collections:
		for collection in collections:
			parsed = parser.get_articles_from_rss(
				'https://medium.com/feed/{}'.format(collection), 'medium')
			
			for article in parsed:
				if article['title'] not in titles:
					titles.append(article['title'])
					articles.append(article)
	else:
		parsed = parser.get_articles_from_rss(
			'https://medium.com/feed/frontpage-picks', 'medium')
		for article in parsed:
			titles.append(article['title'])
			articles.append(article)
	
	return articles
