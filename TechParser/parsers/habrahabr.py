#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'habrahabr'

def get_articles(hubs=[]):
	
	if not hubs:
		return parser.get_articles_from_rss('http://habrahabr.ru/rss/hubs',
			'habrahabr')
	else:
		posts = []
		url = 'http://habrahabr.ru/rss/hub/'
		for hub in hubs:
			for post in parser.get_articles_from_rss(url + hub, SHORT_NAME):
				if post not in posts:
					posts.append(post)
		
		return posts
