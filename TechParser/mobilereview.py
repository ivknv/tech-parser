#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles():
	articles = []
	urls = ['http://mobile-review.com.feedsportal.com/c/33244/f/556830/index.rss',
			'http://mobile-review.com.feedsportal.com/c/33244/f/557686/index.rss',
			'http://mobile-review.com.feedsportal.com/c/33244/f/557683/index.rss']
	for url in urls:
		articles += parser.get_articles_from_rss(url, 'mobile-review')
	
	return articles
