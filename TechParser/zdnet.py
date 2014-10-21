#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles():
	urls = ['http://www.zdnet.com/news/rss.xml',
		'http://downloads.zdnet.com/recent/?mode=rss',
		'http://www.zdnet.com/reviews/rss.xml']
	
	articles = []
	
	for url in urls:
		for article in parser.get_articles_from_rss(url, 'zdnet'):
			if not article in articles:
				articles.append(article)
	
	return articles
