#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser

def get_articles():
	articles = []
	urls = ['http://img.helpix.ru/news/shtml/rss.xml',
			'http://helpix.ru/rss/review-helpix.xml']
	for url in urls:
		res = feedparser.parse(url)
		
		articles += [{'title': i['title'],
					'link': i['link'],
					'source': 'helpix'} for i in res['entries']]
	
	return articles
