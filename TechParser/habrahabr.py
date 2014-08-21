#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	g.go("http://habrahabr.ru")
	
	pages = [""]
	pages += [page.get("href") for page in g.css_list("#nav-pages li a")]
	
	posts = []
	
	for page in pages:
		g.go("http://habrahabr.ru"+page)
		
		posts += parser.get_articles(
			g, ".post .title .post_title",
			".post .title .post_title", "habrahabr")
		
	return posts
