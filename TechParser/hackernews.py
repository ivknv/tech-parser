#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser
import grab

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	
	css_path = ".title a:not()"
	
	for i in range(start_page-1, end_page+1):
		n = 30 * i
		
		g.go("https://news.ycombinator.com/newest?n=%d" %n)
		
		posts += parser.get_articles(g, css_path, css_path, "hackernews")
	
	for post in posts:
		if post["title"].lower() == "more":
			posts.remove(post)
	
	return posts
