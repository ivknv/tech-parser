#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://www.theverge.com")
	
	posts = []
	
	css_paths = [(".storybox article .title a", ""),
		("#hero #seven-feature .feature-box .feature-meta h2 a", ""),
		(".hero-feature .feature-meta h2 a", ""),
		("#quick-reads .pane .slider .quick-read a", ".quick-read-meta h3"),
		(".streams .pane .slider .entry a", ".entry-meta h3")]
	
	for (link_path, title_path) in css_paths:
		posts += parser.get_articles(g, link_path, link_path+title_path,
			"theverge", "www.theverge.com")
	
	return posts
