#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles(hubs=[]):
	
	if not hubs:
		return parser.get_articles_from_rss('http://geektimes.ru/rss/hubs',
			'geektimes')
	else:
		posts = []
		url = 'http://geektimes.ru/rss/hub/'
		for hub in hubs:
			for post in parser.get_articles_from_rss(url + hub, 'geektimes'):
				if post not in posts:
					posts.append(post)
		
		return posts
