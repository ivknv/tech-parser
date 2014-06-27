#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def get_articles():
	g = grab.Grab()
	
	g.setup(hammer_mode=True, hammer_timeouts=((10, 15), (20, 30), (25, 40)))
	
	g.go("http://habrahabr.ru")
	
	pages = g.css_list("#nav-pages li a")
	
	posts = []
	
	for page in pages:
		g.go("http://habrahabr.ru"+page.get("href"))
		articles = g.css_list(".post")
		
		for post in articles:
			post_link = post.cssselect(".title .post_title")[0].get("href")
			title = post.cssselect(".title .post_title")[0].text_content()
			tags = post.cssselect(".tags li a")
			hubs = post.cssselect(".hubs")
			
			posts.append(
				{
					"title": unicode_(title),
					"tags": [[tag.get('href'), unicode_(tag.text_content())] for tag in tags],
					"hubs": [[hub.get('href'), unicode_(hub.text_content())] for hub in hubs],
					"link": post_link,
					"source": "habrahabr"
				}
			)
	return posts
