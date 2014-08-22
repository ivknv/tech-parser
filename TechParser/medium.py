#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(collections=[]):
	g = grab.Grab()
	parser.setup_grab(g)
	
	articles = []
	
	if collections:
		css_path = 'li.bucket-item .postItem .postItem-title a'
		
		for collection in collections:
			g.go('https://medium.com/%s' %collection)
			
			for article in parser.get_articles(g, css_path, css_path,
				'medium', 'medium.com'):
				if article not in articles:
					articles.append(article)
	else:
		css_path = 'div.block-content .block-title a'
		g.go('https://medium.com')
		articles += parser.get_articles(g, css_path, css_path,
			'medium', 'medium.com')
	
	return articles
