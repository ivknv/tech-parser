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
		g.go("http://www.androidcentral.com/content?page=%i" %i)
		
		articles_1 = g.css_list(".node-article .node-inner .title-byline .title a")
		
		for article_link in articles_1:
			title = unicode_(article_link.text_content())
			link = article_link.get("href")
			
			if link.startswith("/"):
				link = "http://www.androidcentral.com" + link
			
			articles.append(
				{
					"link": link,
					"title": title,
					"date": "",
					"source": "androidcentral"
				}
			)
	
	return articles
