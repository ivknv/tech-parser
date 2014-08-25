#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	articles = []
	css_path = '''#news .content-block-data .header td a,
	              #dontmiss .content-block-data .header td a,
	              #reviews .content-block-data .header td a'''
	summary_path = '.content-block-data .teaser'
	
	g.go('http://www.3dnews.ru')
	articles += parser.get_articles(g, css_path, css_path,
		'threednews', 'www.3dnews.ru', summary_path)
	
	return articles
