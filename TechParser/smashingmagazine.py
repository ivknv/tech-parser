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
	
	g.go("http://www.smashingmagazine.com")
	
	css_path = ".post h2 a"

	summary_texts = []
	for elem in g.css_list(".post"):
		text = ''
		for children in elem.getchildren()[2:]:
			text += unicode_(children.text_content()).strip()
		summary_texts.append(parser.cut_text(text))
			
	posts = []
	
	posts = parser.get_articles(g, css_path, css_path, "smashingmagazine",
		"www.smashingmagazine.com")
	for (post, summary) in zip(posts, summary_texts):
		post["summary"] = summary
	
	return posts
