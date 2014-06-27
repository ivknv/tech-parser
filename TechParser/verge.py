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
	
	g.go("http://www.theverge.com")
	
	articles = []
	
	articles_1 = g.css_list(
		"#hero #seven-feature .feature-box .feature-meta h2 a"
	)
	articles_2 = g.css_list(".storybox article .title a")
	articles_3 = g.css_list(
		".hero-feature .feature-meta h2 a"
	)
	
	articles_parsed_1 = [articles_1, articles_2, articles_3]
	
	quick_read = g.css_list("#quick-reads .pane .slider .quick-read a")
	story_streams = g.css_list(".streams .pane .slider .entry a")
	
	articles_parsed_2 = [quick_read, story_streams]
	
	for articles_ in articles_parsed_1:
		for article_link in articles_:
			title = unicode_(article_link.text_content())
			link = article_link.get("href")
			
			articles.append(
				{
					"link": link,
					"title": title,
					"source": "theverge"
				}
			)
	
	for articles_ in articles_parsed_2:
		for article in articles_:
			link = article.get("href")
			try:
				title = unicode_(
					article.cssselect(".quick-read-meta h3")[0].text_content()
				)
			except IndexError:
				title = unicode_(
					article.cssselect(".entry-meta h3")[0].text_content()
				)
		
			articles.append(
				{
					"link": link,
					"title": title,
					"source": "theverge"
				}
			)
	
	return articles
