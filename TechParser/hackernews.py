#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	
	css_path = "tr .title a"
	
	for i in range(start_page, end_page+1):
		g.go("https://news.ycombinator.com/news?p=%d" %i)
		
		posts += parser.get_articles(g, css_path, css_path,
			"hackernews", "news.ycombinator.com")
	
	for post in posts:
		if post["title"].lower() == "more":
			posts.remove(post)
	
	return posts
