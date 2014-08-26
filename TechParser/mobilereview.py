#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser.parser import cut_text, remove_tags, parse_article_image

def get_articles():
	articles = []
	urls = ['http://mobile-review.com.feedsportal.com/c/33244/f/556830/index.rss',
			'http://mobile-review.com.feedsportal.com/c/33244/f/557686/index.rss',
			'http://mobile-review.com.feedsportal.com/c/33244/f/557683/index.rss']
	for url in urls:
		res = feedparser.parse(url)
		
		articles += [{'title': i['title'],
					'link': i['link'],
					'source': 'mobile-review',
					'summary': parse_article_image(i['summary']).decode() +
						cut_text(remove_tags(i['summary']))}
						for i in res['entries']]
	
	return articles
