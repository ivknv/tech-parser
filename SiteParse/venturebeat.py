#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def get_articles():
	g = grab.Grab()
	
	g.go("http://venturebeat.com")
	
	articles = []
	
	featured = g.css_list("#vb-featured li")
	latest_news = g.css_list(".post .entry-wrapper")
	most_popular = g.css_list("ul.most-popular li h2 a")
	editors_pick = g.css_list("ul.editors-pick li h2 a")
	
	for article in featured:
		article_link = article.cssselect("a")[0]
		
		title = unicode_(article_link.cssselect(
			"span.snipe-wrapper h2.title"
		)[0].text_content())
		date = unicode_(article_link.cssselect(
			"span.snipe-wrapper span.date"
		)[0].text_content())
		
		link = article_link.get("href")
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": date,
				"source": "venturebeat"
			}
		)
	
	for article in most_popular:
		title = unicode_(article.get("title"))
		link = article.get("href")
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": "",
				"source": "venturebeat"
			}
		)
	
	for article in editors_pick:
		title = unicode_(article.get("title"))
		link = article.get("href")
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": "",
				"source": "venturebeat"
			}
		)
	
	for article in latest_news:
		article_link = article.cssselect(
			".entry-header .entry-title a"
		)[0]
		
		title = unicode_(article_link.text_content())
		date = unicode_(article.cssselect(
			".entry-header .entry-meta .the-time"
		)[0].text_content())
		
		link = article_link.get("href")
		
		articles.append(
			{
				"link": link,
				"title": title,
				"date": date,
				"source": "venturebeat"
			}
		)
	
	return articles
