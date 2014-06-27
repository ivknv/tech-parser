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
	
	for page_num in range(start_page, end_page+1):
		g.go("http://engadget.com/page/%i" %page_num)
		
		article_elements = g.css_list(".post")
		
		for article in article_elements:
			article_link = article.cssselect(".headline .h2 a")[0]
			
			title = unicode_(article_link.text_content())
			link = article_link.get("href")
		
			articles.append(
				{
					"link": link,
					"title": title,
					"source": "engadget"
				}
			)
	
	return articles
