#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab

def get_articles():
	g = grab.Grab()
	g.go("http://readwrite.com")
	
	articles = []
	
	top_story = g.css(".story.view-hero header")
	
	top_title = top_story.cssselect("h1 a")[0]
	top_link = top_title.text_content()
	top_title = top_title.text_content()
	
	articles.append(
		{
			"link": top_link,
			"title": top_title,
			"source": "readwrite"
		}
	)
	
	stories = g.css_list("article")
	
	for article in stories:
		try:
			category = article.cssselect("h3")[0].text_content()
		except IndexError:
			try:
				category = article.cssselect("header .meta .section .dd a.parsed")[0].text_content()
			except IndexError:
				category = ""
		
		try:
			title = article.cssselect("h1 a")[0]
		except IndexError:
			title = article.cssselect("header .grid-item h1 a")[0]
		
		link = title.get("href")
		title = title.text_content()
		
		try:
			date = article.cssselect("header .meta .publish-date")[0].text_content()
		except IndexError:
			date = ""
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": date,
				"category": category,
				"source": "readwrite"
			}
		)
	
	return articles
