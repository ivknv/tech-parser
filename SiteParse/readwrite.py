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
	
	g.go("http://readwrite.com")
	
	articles = []
	
	top_story = g.css(".story.view-hero header")
	
	top_title = top_story.cssselect("h1 a")[0]
	top_link = unicode_(top_title.text_content())
	top_title = unicode_(top_title.text_content())
	
	if top_link.startswith("/"):
		top_link = "http://readwrite.com" + top_link
	
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
			category = unicode_(article.cssselect("h3")[0].text_content())
		except IndexError:
			try:
				category = unicode_(
					article.cssselect(
						"header .meta .section .dd a.parsed"
					)[0].text_content()
				)
			except IndexError:
				category = ""
		
		try:
			title = article.cssselect("h1 a")[0]
		except IndexError:
			title = article.cssselect("header .grid-item h1 a")[0]
		
		link = title.get("href")
		
		if link.startswith("/"):
			link = "http://readwrite.com" + link
		
		title = unicode_(title.text_content())
		
		try:
			date = unicode_(
				article.cssselect(
					"header .meta .publish-date"
				)[0].text_content()
			)
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
