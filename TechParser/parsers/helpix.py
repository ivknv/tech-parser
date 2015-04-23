#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'helpix'

def get_articles():
	articles = []
	urls = ['http://img.helpix.ru/news/shtml/rss.xml',
			'http://helpix.ru/rss/review-helpix.xml']
	
	for url in urls:
		articles += parser.get_articles_from_rss(url, SHORT_NAME)
	
	return articles
