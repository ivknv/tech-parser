#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles():
	articles = parser.parse_rss('http://www.theverge.com/rss/frontpage',
		'theverge')
	for article in articles:
		article['fromrss'] = 0
	
	return articles
