#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=1):
	g = grab.Grab()
	parser.setup_grab(g)
	
	articles = []
	css_path = '#slider .slider-article li figcaption h3 a, article header h2 a'
	
	for i in range(start_page, end_page+1):
		g.go('http://redroid.ru/category/news/page/%i' %i)
		found_articles = parser.get_articles(g, css_path, css_path,
			'redroid', 'redroid.ru')
		
		for article in found_articles:
			if article not in articles:
				articles.append(article)
	
	return articles
