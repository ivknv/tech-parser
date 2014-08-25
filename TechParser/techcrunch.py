#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://techcrunch.com")
	
	posts = []
	links = []
	
	css_paths = [(".island .plain-feature a", ".block-title h2"),
		(".island .plain-item-list li a", ".plain-title h2"),]
	
	for (link_path, title_path) in css_paths:
		posts += parser.get_articles(
			g, link_path, link_path+title_path, "techcrunch")
	
	g.go("http://techcrunch.com/popular")
	
	css_path1 = ".river .river-block .block .block-content h2.post-title a"
	summary_path = ".river .river-block .block .block-content p.excerpt"
	
	posts += parser.get_articles(g, css_path1, css_path1,
		"techcrunch", "techcrunch.com", summary_path)
	
	for post in posts:
		
		if not post["link"] in links:
			links.append(post["link"])
		else:
			posts.remove(post)
		
	return posts
