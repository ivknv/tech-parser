#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import grab
from TechParser import parser

def get_articles(browser="firefox"):
	browsers = {"firefox": webdriver.Firefox,
		"chrome": webdriver.Chrome}
	
	driver = browsers[browser]()
	driver.get("http://readwrite.com")
	
	g = grab.Grab(driver.page_source)
	
	driver.quit()
	
	posts = []
	
	css_path = ".m-story.mm-feature .m-item--hed a"
	
	posts += parser.get_articles(g,
		css_path, css_path, "readwrite")
	
	posts += parser.get_articles(g, css_path, css_path, "readwrite",
		"readwrite.com")
	posts += parser.get_articles(g, css_path, css_path, "readwrite",
		"readwrite.com")
	
	return posts
