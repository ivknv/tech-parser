#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	
	for page_num in range(start_page, end_page+1):
		g.go("http://engadget.com/page/%i" %page_num)
		
		css_path = ".post .headline .h2 a"
		
		posts += parser.get_articles(g, css_path, css_path, "engadget")
	
	return posts
