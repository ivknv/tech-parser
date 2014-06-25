#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def get_articles():
	g = grab.Grab()
	g.go("http://techcrunch.com")
	
	articles = []
	links = []
	
	articles_1 = g.css_list(".island .plain-feature a")
	articles_2 = g.css_list(".island .plain-item-list li a")
	latest = g.css_list(".river .river-block .block")
	
	for article in articles_1:
		link = article.get("href")
		if not link in links:
			links.append(link)
		else:
			continue
		
		title = unicode_(article.cssselect(".block-title h2")[0].text_content())
		
		articles.append({
			"link": link,
			"title": title,
			"date": "",
			"source": "techcrunch"
		})
	
	for article in articles_2:
		link = article.get("href")
		if not link in links:
			links.append(link)
		else:
			continue
		
		title = unicode_(article.cssselect(".plain-title h2")[0].text_content())
		
		articles.append({
			"link": link,
			"title": title,
			"date": "",
			"source": "techcrunch"
		})
	
	for article in latest:
		try:
			title = article.cssselect(".block-content .post-title a")[0]
		except IndexError:
			title = article.cssselect(".block-content-brief .post-title a")[0]
		
		link = title.get("href")
		if not link in links:
			links.append(link)
		else:
			continue
		
		title = unicode_(title.text_content())
		
		tags = article.cssselect(".tags .tag")
		tags = [
				[tag.get("href"),
				unicode_(tag.cssselect("span")[0].text_content())]
				for tag in tags
				]
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": "",
				"tags": tags,
				"source": "techcrunch"
			}
		)
	
	g.go("http://techcrunch.com/popular")
	
	popular = g.css_list("ul.river .river-block .block .block-content")
	
	for article in popular:
		title = article.cssselect(".post-title a")[0]
		link = title.get("href")
		
		if not link in links:
			links.append(link)
		else:
			continue
		
		title = unicode_(title.text_content())
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": "",
				"source": "techcrunch"
			}
		)
	
	return articles
