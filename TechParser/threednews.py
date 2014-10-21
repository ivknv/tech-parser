#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles():
	articles = []
	
	urls = ['http://www.3dnews.ru/news/rss',
		'http://www.3dnews.ru/software-news/rss']
	
	for url in urls:
		for article in parser.get_articles_from_rss(url, 'threednews'):
			if not article in articles:
				articles.append(article)
	
	return articles
