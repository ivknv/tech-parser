#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	g.go("http://it.toolbox.com")
	
	css_path = ".tile .tileContent div:first-child .floatleft:nth-child(2) a"
	
	posts = parser.get_articles(g, css_path, css_path, "ittoolbox")
	
	return posts
