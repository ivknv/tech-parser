#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=2):
	g = grab.Grab()
	parser.setup_grab(g)
	
	articles = []
	css_path = '.single .title h2 a'
	summary_path = '.single .cover .entry'
	
	for i in range(start_page, end_page+1):
		g.go('http://droider.ru/category/news/page/%i' %i)
		articles += parser.get_articles(g, css_path, css_path,
			'droider', 'droider.ru', summary_path)
	
	return articles
