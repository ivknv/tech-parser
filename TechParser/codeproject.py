#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=1):
	g = grab.Grab()
	parser.setup_grab(g)
	
	posts = []
	css_path = "tr td .content-list-item .title a"
	summary_path = ".content-list-item .description"
	
	for i in range(start_page, end_page+1):
		g.go("http://www.codeproject.com/script/Articles/Latest.aspx?pgnum=%d"
			%i)
		
		posts += parser.get_articles(g, css_path, css_path,
			"codeproject", "www.codeproject.com", summary_path)
	
	return posts
