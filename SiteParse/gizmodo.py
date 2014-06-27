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
	
	g.go("http://gizmodo.com")
	
	articles = []
	
	popular_stories = g.css_list(".row.sidebar-item.js_sidebar-element .column .headline a")
	posts = g.css_list("article.post.hentry.js_post-item header .headline a")
	
	links = []
	
	for article in popular_stories:
		link = article.get("href")
		links.append(link)
		
		title = unicode_(article.text_content())
		
		articles.append(
			{
				"link": link,
				"title": title,
				"source": "gizmodo"
			}
		)
	
	for article in posts:
		link = article.get("href")
		
		if not link in links:
			links.append(link)
		else:
			continue
		
		title = unicode_(article.text_content())
		
		articles.append(
			{
				"link": link,
				"title": title,
				"source": "gizmodo"
			}
		)
	
	return articles
