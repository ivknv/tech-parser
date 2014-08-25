#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=1):
	
	g = grab.Grab()
	parser.setup_grab(g)
	
	posts = []
	css_path = ".ourSingle h2 a"
	summary_path = ".ourSingle p:nth-child(5)"
	
	for i in range(start_page, end_page+1):
		g.go("http://topdesignmag.com/page/%d" %i)
		
		posts += parser.get_articles(g, css_path, css_path,
			"topdesignmagazine", "topdesignmag.com", summary_path)
	
	return posts
