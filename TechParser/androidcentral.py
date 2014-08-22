#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	
	for i in range(start_page, end_page+1):
		g.go("http://www.androidcentral.com/content?page=%i" %i)
		
		css_path = ".node-article .node-inner .title-byline .title a"
		
		articles = parser.get_articles(g, css_path, css_path,
			"androidcentral", "www.androidcentral.com")
		
		posts += articles
	
	return posts
