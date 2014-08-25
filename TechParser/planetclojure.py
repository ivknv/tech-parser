#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def concat_texts(x, y):
	if not isinstance(x, str): return x.text_content() + y.text_content()
	else: return x + y.text_content(),

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
