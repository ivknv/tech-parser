#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://techrepublic.com")
	
	posts = []
	
	css_paths = ["#haccordion .viewport section .slide .lead-in h3 a",
		"#feature-hubs .item-list .row .item .title a",
		"#article-river #tab-content-1 .items li .item-content .title a",
		"#article-river #tab-content-2 .items li .item-content .title a"
	]
	
	for css_path in css_paths:
		posts += parser.get_articles(g, css_path, css_path, "techrepublic")
	
	for i in range(len(posts)):
		link = posts[i]["link"]
		
		if link.startswith("/"):
			link = "http://techrepublic.com" + link
			posts[i]["link"] = link
	
	return posts