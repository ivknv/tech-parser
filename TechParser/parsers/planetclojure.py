#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser
from TechParser.py2x import unicode_

def get_articles():
	g = grab.Grab()
	parser.setup_grab(g)
	
	g.go('http://planet.clojure.in')
	
	css_path = '.entry .article > h2 a'
	summary_texts = []
	for elem in g.css_list(".entry .article"):
		text = ''
		for children in elem.getchildren()[1:-1]:
			text += unicode_(children.text_content()).strip()
		summary_texts.append(parser.cut_text(text))
			
	posts = parser.get_articles(g, css_path, css_path,
		'planetclojure', 'planet.clojure.in')
	
	for (post, summary_text) in zip(posts, summary_texts):
		post['summary'] = summary_text
	
	return posts
