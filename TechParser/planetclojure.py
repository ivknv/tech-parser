#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go('http://planet.clojure.in')
	
	css_path = '.entry .article h2 a'
	
	return parser.get_articles(g, css_path, css_path,
		'planetclojure', 'planet.clojure.in')
