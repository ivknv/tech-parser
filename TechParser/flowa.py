#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go("http://flowa.fi")
	
	link_path = ".article-container a"
	title_path = link_path + " .article .article-heading .heading-container h2"
	
	posts = parser.get_articles(g, link_path, title_path, "flowa")
	
	link_path = ".main-article a:not(#blog-entries-top)"
	title_path  = link_path + " div .article-par .article-par-container .heading-container h2"
	
	posts += parser.get_articles(g, link_path, title_path, "flowa")
	
	return posts
