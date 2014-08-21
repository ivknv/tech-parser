#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://www.smashingmagazine.com")
	
	css_path = ".post h2 a"
	posts = parser.get_articles(g, css_path, css_path, "smashingmagazine",
		"www.smashingmagazine.com")	
	
	return posts
