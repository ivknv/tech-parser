#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import grab
import parser

def get_articles(browser="firefox"):
	browsers = {"firefox": webdriver.Firefox,
		"chrome": webdriver.Chrome}
	
	driver = browsers[browser]()
	driver.get("http://readwrite.com")
	
	g = grab.Grab(driver.page_source)
	
	posts = []
	
	css_path = ".m-story.mm-feature .m-item--hed a"
	
	posts += parser.get_articles(g,
		css_path, css_path, "readwrite")
	
	posts += parser.get_articles(g, css_path, css_path, "readwrite")
	posts += parser.get_articles(g, css_path, css_path, "readwrite")
		
	for i in range(len(posts)):
		link = posts[i]["link"]
		if link.startswith("/"):
			link = "http://readwrite.com" + link
			posts[i]["link"] = link
	
	return posts
