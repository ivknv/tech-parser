#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=3):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://venturebeat.com")
	
	posts = []
	
	css_paths = [("#vb-featured li a", "span.snipe-wrapper h2.title"),
		(".post .entry-wrapper .entry-header .entry-title a", ""),
		("ul.most-popular li h2 a", ""),
		("ul.editors-pick li h2 a", "")]
	
	if start_page == 1:
		for (link_path, title_path) in css_paths:
			posts += parser.get_articles(g,
				link_path, link_path+title_path, "venturebeat")
	
	for i in range(start_page+1, end_page+1):
		g.go("http://venturebeat.com/page/%i" %i)
		
		posts += parser.get_articles(g,
			css_paths[1][0], css_paths[1][0], "venturebeat")
	
	return posts
