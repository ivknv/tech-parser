#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go("http://www.maketecheasier.com")
	
	css_path = ".post .entry-header .entry-title a"
	summary_path = ".post .entry-content p"
	
	posts = parser.get_articles(g, css_path, css_path,
		"maketecheasier", "www.maketecheasier.com", summary_path)
	
	return posts
