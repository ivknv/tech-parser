#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(end_page=3):
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go('http://trashbox.ru/public/b_news')
	
	articles = []
	
	current_page = int(g.css_text('.span_navigator_pages .span_item_active'))
	pages = range(current_page - end_page + 1, current_page + 1)
	
	css_path = '.td2 .h_topic_caption a'
	summary_path = '.div_topic .div_text'
	
	for page in pages:
		g.go('http://trashbox.ru/public/b_news/page_topics/%s' %page)
		
		articles += parser.get_articles(g, css_path, css_path,
			'trashbox', 'trashbox.ru', summary_path)
	
	return articles
