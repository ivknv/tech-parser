#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser
import grab

def get_articles(start_page=1, end_page=1):
	g = grab.Grab()
	parser.setup_grab(g)
	
	posts = []
	
	for i in range(start_page, end_page+1):
		g.go("http://www.codeproject.com/script/Articles/Latest.aspx?pgnum=%d"
				%i)
		
		css_path = "tr td .content-list-item .title a"
		
		posts += parser.get_articles(g, css_path, css_path, "codeproject")
	
	for i in range(len(posts)):
		link = posts[i]["link"]
		
		if link.startswith("/"):
			link = "http://www.codeproject.com" + link
			posts[i]["link"] = link
	
	return posts
