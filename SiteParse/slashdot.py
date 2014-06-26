#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	g.setup(hammer_mode=True, hammer_timeouts=((10, 15), (20, 30), (25, 40)))
	
	articles = []
	
	for i in range(start_page, end_page+1):
		g.go("http://slashdot.org?page=%i" %i)
		posts = g.css_list(".article")
		
		for post in posts:
			post_link = post.cssselect("header h2.story span a")[0]
			
			title = unicode_(post_link.text_content())
			date = unicode_(post.cssselect("header .details time")[0].text_content())
			
			link = post_link.get("href")
			
			if link.startswith("//"):
				link = "http:%s" %link
			
			articles.append(
				{
					"link": link,
					"title": title,
					"date": date,
					"source": "slashdot"
				}
			)
	return articles
