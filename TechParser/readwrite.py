#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://readwrite.com")
	
	posts = []
	
	top_story_path = ".story.view-hero header h1 a"
	
	posts += parser.get_articles(g,
		top_story_path, top_story_path, "readwrite")
	
	css_path1 = "article h1 a"
	css_path2 = "article header .grid-item h1 a"
	
	posts += parser.get_articles(g, css_path1, css_path1, "readwrite")
	posts += parser.get_articles(g, css_path2, css_path2, "readwrite")
		
	for i in range(len(posts)):
		link = posts[i]["link"]
		if link.startswith("/"):
			link = "http://readwrite.com" + link
			posts[i]["link"] = link
	
	return posts
