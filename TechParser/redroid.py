#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser
from lxml.etree import tostring

def get_articles(start_page=1, end_page=1):
	g = grab.Grab()
	parser.setup_grab(g)
	
	articles = []
	css_paths = [('#slider .slider-article li figcaption h3 a',
		'', '#slider .slider-article li figure a img'),
		('#article article header h2 a', 'article header p',
			'#article article figure a img')]
	
	for i in range(start_page, end_page+1):
		g.go('http://redroid.ru/category/news/page/%i' %i)
		for (css_path, summary_path, image_path) in css_paths:
			found_articles = parser.get_articles(g, css_path, css_path,
				'redroid', 'redroid.ru', summary_path)
			
			article_images = map(lambda x: tostring(x).decode(), g.css_list(image_path))
		
			for (article, img) in zip(found_articles, article_images):
				if article not in articles:
					article['summary'] = img + article['summary']
					articles.append(article)
	
	return articles
