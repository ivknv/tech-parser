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
	
	g.go("http://www.smashingmagazine.com")
	
	articles = []
	
	posts = g.css_list(".post")
	
	for post in posts:
		title = post.cssselect("h2 a")[0]
		link = title.get("href")
		
		if link.startswith("/"):
			link = "http://www.smashingmagazine.com" + link
		
		title = unicode_(title.text_content())
		date = unicode_(post.cssselect(".pmd li.date")[0].text_content())
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": date,
				"source": "smashingmagazine"
			}
		)
	
	return articles
