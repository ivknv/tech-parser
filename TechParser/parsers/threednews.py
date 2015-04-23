#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'threednews'

def get_articles():
	articles = []
	
	urls = ['http://www.3dnews.ru/news/rss',
		'http://www.3dnews.ru/software-news/rss']
	
	for url in urls:
		for article in parser.get_articles_from_rss(url, SHORT_NAME):
			if not article in articles:
				articles.append(article)
	
	return articles
