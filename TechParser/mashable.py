#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://mashable.com")
	
	css_path = "article header hgroup h1 a"
	
	posts = parser.get_articles(g, css_path, css_path,
		"mashable", "mashable.com")
	
	return posts
