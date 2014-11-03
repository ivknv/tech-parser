#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles(categories=['all']):
	urls = {'news': 'http://www.zdnet.com/news/rss.xml',
		'downloads': 'http://downloads.zdnet.com/recent/?mode=rss',
		'reviews': 'http://www.zdnet.com/reviews/rss.xml'}
	
	if 'all' in categories:
		categories = ['news', 'downloads', 'reviews']
	
	articles = []
	
	for categorie in categories:
		url = urls[categorie]
		for article in parser.get_articles_from_rss(url, 'zdnet'):
			if not article in articles:
				articles.append(article)
	
	return articles
