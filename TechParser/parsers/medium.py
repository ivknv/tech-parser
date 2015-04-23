#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'medium'

def get_articles(collections=[]):
	articles = []
	titles = []
	
	if collections:
		for collection in collections:
			parsed = parser.get_articles_from_rss(
				'https://medium.com/feed/{}'.format(collection), SHORT_NAME)
			
			for article in parsed:
				if article['title'] not in titles:
					titles.append(article['title'])
					articles.append(article)
	else:
		parsed = parser.get_articles_from_rss(
			'https://medium.com/feed/frontpage-picks', SHORT_NAME)
		for article in parsed:
			titles.append(article['title'])
			articles.append(article)
	
	return articles
