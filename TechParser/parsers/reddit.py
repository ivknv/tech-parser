#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'reddit'

def get_articles(reddits=['tech']):
	articles = []
	links = []
	
	for r in reddits:
		parsed = parser.get_articles_from_rss(
			'http://www.reddit.com/r/{}/.rss'.format(r), SHORT_NAME)
		for article in parsed:
			if article['link'] not in links:
				links.append(article['link'])
				articles.append(article)
	
	return articles
