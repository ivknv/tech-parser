#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def get_articles(start_page=1, end_page=3):
	g = grab.Grab()
	
	g.setup(hammer_mode=True, hammer_timeouts=((10, 15), (20, 30), (25, 40)))
	
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
		
		link = article_link.get("href")
		
		articles.append(
			{
				"link": link,
				"title": title,
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
				"source": "venturebeat"
			}
		)
	
	for article in latest_news:
		article_link = article.cssselect(
			".entry-header .entry-title a"
		)[0]
		
		title = unicode_(article_link.text_content())
		
		link = article_link.get("href")
		
		articles.append(
			{
				"link": link,
				"title": title,
				"source": "venturebeat"
			}
		)
	
	for i in range(start_page+1, end_page+1):
		g.go("http://venturebeat.com/page/%i" %i)
		
		articles_1 = g.css_list("#content .post .entry-wrapper .entry-header")
		
		for article in articles_1:
			date = unicode_(article.cssselect(
				".entry-meta .the-time"
			)[0].text_content())
			
			title = article.cssselect(".entry-title a")[0]
			link = title.get("href")
			title = unicode_(title.text_content())
			
			articles.append(
				{
					"link": link,
					"title": title,
					"source": "venturebeat"
				}
			)
	
	return articles
