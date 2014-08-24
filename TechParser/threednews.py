#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	articles = []
	css_path = '.header td a'
	
	g.go('http://www.3dnews.ru')
	articles += parser.get_articles(g, css_path, css_path,
		'threednews', 'www.3dnews.ru')
	
	return articles
