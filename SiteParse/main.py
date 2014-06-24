#!/usr/bin/env python
# -*- coding: utf-8 -*-

import habrahabr
import engadget
import slashdot
import venturebeat

import os

from random import shuffle

from distutils.dir_util import copy_tree

from django.core.paginator import Paginator

from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories="templates", default_filters=["decode.utf8"], input_encoding="utf-8", output_encoding="utf-8")

main_page = mylookup.get_template("articles.html")

if __name__ == "__main__":
	print("Please wait...")
	
	print("Parsing articles from Habrahabr...")
	habrahabr_articles = habrahabr.get_articles()
	
	print("Parsing articles from VentureBeat...")
	venturebeat_articles = venturebeat.get_articles()
	
	print("Parsing articles from Engadget...")
	engadget_articles = engadget.get_articles()
	
	print("Parsing articles from Slashdot...")
	slashdot_articles = slashdot.get_articles()
	
	articles = habrahabr_articles + engadget_articles + \
	slashdot_articles + venturebeat_articles
	
	shuffle(articles)
	
	articles = Paginator(articles, 20)
	
	print("Writting data...")
	
	if not os.path.exists("output"):
		os.mkdir("output")
	
	copy_tree(src="templates/icons", dst="output/icons")
	
	styles = open("templates/style.css")
	styles_content = styles.read()
	styles.close()
	
	styles = open("output/style.css", "w")
	styles.write(styles_content)
	styles.close()
	
	for i in range(1, articles.num_pages+1):
		page = articles.page(i)
		
		next_page = i+1 if i < articles.num_pages else None
		previous_page = i-1 if i > 1 else None
		
		f = open("output/output%s.html" %i, "w")
		f.write(
			main_page.render(
				articles=page,
				next_page=next_page,
				previous_page=previous_page
			)
		)
		f.close()
	print("Go check output/output1.html")
