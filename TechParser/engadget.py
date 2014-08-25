#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	css_path = ".post .headline .h2 a"
	summary_path = ".post .post-body .copy"
	
	for page_num in range(start_page, end_page+1):
		g.go("http://engadget.com/page/%i" %page_num)
		
		posts += parser.get_articles(g, css_path, css_path, "engadget",
			summary_path=summary_path)
	
	return posts
