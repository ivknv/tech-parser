#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser import parser

def get_articles(collections=[]):
	articles = []
	titles = []
	
	if collections:
		for collection in collections:
			parsed = feedparser.parse('https://medium.com/feed/{}'.format(collection))
			
			for article in parsed['entries']:
				if article['title'] not in titles:
					summary = article['summary']
					titles.append(article['title'])
					articles.append({'title': article['title'],
						'link': article['link'],
						'source': 'medium',
						'summary': summary})
	else:
		parsed = feedparser.parse('https://medium.com/feed/frontpage-picks')
		for article in parsed['entries']:
			summary = article['summary']
			titles.append(article['title'])
			articles.append({'title': article['title'],
				'link': article['link'],
				'source': 'medium',
				'summary': summary})
	
	return articles
