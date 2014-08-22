#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go("http://www.dzone.com")
	
	css_path = ".linkblock .details h3 a[rel=bookmark]"
	
	posts = parser.get_articles(g, css_path, css_path, "dzone")
	
	for i in range(len(posts)):
		link = posts[i]["link"]
		
		if link.startswith("/"):
			link = "http://www.dzone.com" + link
			posts[i]["link"] = link
		posts[i]["title"] = posts[i]["title"].strip()
	
	return posts
