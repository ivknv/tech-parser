#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	css_path = ".node-article .node-inner .title-byline .title a"
	summary_path = ".entry .entry-content .field .field-items"
	
	for i in range(start_page, end_page+1):
		g.go("http://www.androidcentral.com/content?page=%i" %i)
		
		articles = parser.get_articles(g, css_path, css_path,
			"androidcentral", "www.androidcentral.com", summary_path)
		
		posts += articles
	
	return posts
