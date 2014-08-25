#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go("http://digg.com")
	
	css_path = ".story-container .story-content .story-header .story-title .story-title-link"
	summary_path = ".story-container .story-content p.story-description"
	
	posts = parser.get_articles(g, css_path, css_path,
		"digg", summary_path=summary_path)
	
	return posts
