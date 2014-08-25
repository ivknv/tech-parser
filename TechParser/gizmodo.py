#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://gizmodo.com")
	
	posts = []
	
	css_path1 = ".row.sidebar-item.js_sidebar-element .column .headline a"
	css_path2 = "article.post.hentry.js_post-item header .headline a"
	summary_path = ".columns p.first-text"
	
	posts += parser.get_articles(g, css_path1, css_path1,
		"gizmodo", "gizmodo.com", summary_path)
	posts += parser.get_articles(g, css_path2, css_path2,
		"gizmodo", "gizmodo.com", summary_path)
	
	links = []
	
	for post in posts:
		if post["link"] not in links:
			links.append(post["link"])
		else:
			posts.remove(post)
	
	return posts
