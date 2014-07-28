#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser
import grab

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go("http://it.toolbox.com")
	
	css_path = ".tile .tileContent div .floatleft a"
	
	posts = parser.get_articles(g, css_path, css_path, "ittoolbox")
	
	return posts
