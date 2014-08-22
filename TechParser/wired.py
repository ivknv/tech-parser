#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go("http://www.wired.com")
	
	css_path = ".headline a"
	
	posts = parser.get_articles(g, css_path, css_path,
		"wired", "www.wired.com")
	
	return posts
