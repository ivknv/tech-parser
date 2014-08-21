#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://www.theverge.com")
	
	posts = []
	
	articles_1 = g.css_list(
		"#hero #seven-feature .feature-box .feature-meta h2 a"
	)
	articles_2 = g.css_list(".storybox article .title a")
	articles_3 = g.css_list(
		".hero-feature .feature-meta h2 a"
	)
	
	quick_read = g.css_list("#quick-reads .pane .slider .quick-read a")
	story_streams = g.css_list(".streams .pane .slider .entry a")
	
	css_paths = [(".storybox article .title a", ""),
		("#hero #seven-feature .feature-box .feature-meta h2 a", ""),
		(".hero-feature .feature-meta h2 a", ""),
		("#quick-reads .pane .slider .quick-read a", ".quick-read-meta h3"),
		(".streams .pane .slider .entry a", ".entry-meta h3")]
	
	for (link_path, title_path) in css_paths:
		posts += parser.get_articles(g,
			link_path, link_path+title_path, "theverge")
	
	return posts
