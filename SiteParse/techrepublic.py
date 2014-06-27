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
	
	g.go("http://techrepublic.com")
	
	articles = []
	
	articles_1 = g.css_list(
		"#haccordion .viewport section .slide .lead-in h3 a"
	)
	editors_pick = g.css_list(
		"#feature-hubs .item-list .row .item .title a"
	)
	latest = g.css_list(
		"#article-river #tab-content-1 .items li .item-content .title a"
	)
	
	most_popular = g.css_list(
		"#article-river #tab-content-2 .items li .item-content .title a"
	)
	
	articles_parsed = [articles_1, editors_pick, latest, most_popular]
	
	for articles_list in articles_parsed:
		for article_title in articles_list:
			link = article_title.get("href")
			
			if link.startswith("/"):
				link = "http://techrepublic.com" + link
			
			title = unicode_(article_title.text_content())
			
			articles.append(
				{
					"link": link,
					"title": title,
					"source": "techrepublic"
				}
			)
	
	return articles
