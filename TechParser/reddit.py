#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(reddits=['tech']):
	g = grab.Grab()
	parser.setup_grab(g)
	
	css_path = 'div.entry p.title a.title'
	
	articles = []
	links = []
	
	for r in reddits:
		g.go('http://www.reddit.com/r/%s' %r)
		
		for article in parser.get_articles(g, css_path, css_path,
			'reddit', 'www.reddit.com'):
			if article['link'] not in links:
				links.append(article['link'])
				articles.append(article)
	
	return articles
