#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser.parser import cut_text, remove_tags

def get_articles():
	urls = ['http://www.zdnet.com/news/rss.xml',
		'http://downloads.zdnet.com/recent/?mode=rss',
		'http://www.zdnet.com/reviews/rss.xml']
	
	articles = []
	titles = []
	
	for url in urls:
		res = feedparser.parse(url).entries
		entries = [{'title': i['title'],
					'link': i['link'],
					'summary': cut_text(remove_tags(i['summary'])),
					'source': 'zdnet'} for i in res]
		for entry in entries:
			if entry['title'].lower() not in titles:
				titles.append(entry['title'].lower())
				articles.append(entry)
	
	return articles
