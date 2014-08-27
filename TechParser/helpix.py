#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser.parser import remove_tags, cut_text, parse_article_image

def get_articles():
	articles = []
	urls = ['http://img.helpix.ru/news/shtml/rss.xml',
			'http://helpix.ru/rss/review-helpix.xml']
	for url in urls:
		res = feedparser.parse(url)
		
		articles += [{'title': i['title'],
					'link': i['link'],
					'source': 'helpix',
					'summary': parse_article_image(i['summary']).decode() +
						cut_text(remove_tags(i['summary']))}
						for i in res['entries']]
	
	return articles
