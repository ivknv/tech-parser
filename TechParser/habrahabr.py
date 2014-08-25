#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(hubs=[]):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	css_path = ".post .title .post_title"
	pg_path = "#nav-pages li a:not(a[rel=nofollow]), #nav-pages li em"
	summary_path = ".post .content"
	posts = []
	
	if not hubs:
		url = "http://habrahabr.ru/posts/top/weekly/"
		g.go(url)
		pages = map(lambda x: str(x.text_content()).strip(),
			g.css_list(pg_path))
		for page in pages:
			g.go(url + "page%s" %page)
			
			posts += parser.get_articles(g, css_path, css_path, "habrahabr",
				summary_path=summary_path)
	else:
		url = "http://habrahabr.ru/hub/"
		for hub in hubs:
			g.go(url + hub)
			pages = map(lambda x: str(x.text_content()).strip(),
				g.css_list(pg_path))
			for page in pages:
				g.go(url + "%s/page%s" %(hub, page))
				for post in parser.get_articles(g, css_path, css_path,
					"habrahabr", summary_path=summary_path):
					if post not in posts:
						posts.append(post)
		
	return posts
