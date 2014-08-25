#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(collections=[]):
	g = grab.Grab()
	parser.setup_grab(g)
	
	articles = []
	titles = []
	
	if collections:
		css_path = 'li.bucket-item .postItem .postItem-title a'
		summary_path = 'li.bucket-item .postItem .postItem-snippet p'
		
		for collection in collections:
			g.go('https://medium.com/%s' %collection)
			
			for article in parser.get_articles(g, css_path, css_path,
				'medium', 'medium.com', summary_path):
				if article['title'] not in titles:
					titles.append(article['title'])
					articles.append(article)
	else:
		css_path = 'div.block-content .block-title a'
		summary_path = 'div.block-content a.block-snippet'
		g.go('https://medium.com')
		articles += parser.get_articles(g, css_path, css_path,
			'medium', 'medium.com', summary_path)
	
	return articles
