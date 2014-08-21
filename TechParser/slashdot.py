#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	css_path = "article header h2 span a"
	
	for i in range(start_page, end_page+1):
		g.go("http://slashdot.org?page=%i" %i)
		
		posts += parser.get_articles(g, css_path, css_path, "slashdot")
		
	return posts
