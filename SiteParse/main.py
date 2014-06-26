#!/usr/bin/env python
# -*- coding: utf-8 -*-

import habrahabr
import engadget
import slashdot
import venturebeat
import gizmodo
import techcrunch
import readwrite

from random import shuffle

import pickle

import sys

from time import time, sleep

from threading import Thread

from django.core.paginator import Paginator

from mako.template import Template
from mako.lookup import TemplateLookup

from bottle import route, run, static_file, default_app

mylookup = TemplateLookup(directories="templates", default_filters=["decode.utf8"], input_encoding="utf-8", output_encoding="utf-8")

articles = []

def dump_articles():
	print("Please wait...")
	
	print("Parsing articles from Habrahabr...")
	habrahabr_articles = habrahabr.get_articles()
	
	print("Parsing articles from VentureBeat...")
	venturebeat_articles = venturebeat.get_articles()
	
	print("Parsing articles from Engadget...")
	engadget_articles = engadget.get_articles()
	
	print("Parsing articles from Slashdot...")
	slashdot_articles = slashdot.get_articles()
	
	print("Parsing articles from Gizmodo...")
	gizmodo_articles = gizmodo.get_articles()
	
	print("Parsing articles from TechCrunch...")
	techcrunch_articles = techcrunch.get_articles()
	
	print("Parsing articles from Read/Write Web...")
	readwrite_articles = readwrite.get_articles()
	
	articles = habrahabr_articles + engadget_articles + \
	slashdot_articles + venturebeat_articles + \
	gizmodo_articles + techcrunch_articles + readwrite_articles
	
	shuffle(articles)
	
	dumped = pickle.dumps(articles)
	f = open("articles_dumped", "w")
	f.write(dumped)
	f.close()

def dump_articles_per_sec(s=30*60):
	while True:
		if int(time()) % s == 0:
			dump_articles()
		sleep(0.5)

def load_articles():
	f = open("articles_dumped")
	dumped = f.read()
	f.close()
	
	articles = pickle.loads(dumped)
	
	return articles

@route('/static/<filename:path>')
def serve_static(filename):
	return static_file(filename, root="static")

@route("/")
@route("/<page_number>")
def articles_list(page_number=1):
	main_page = mylookup.get_template("articles.html")
	
	try:
		page_number = int(page_number)
	except TypeError:
		page_number = 1
	
	try:	
		articles = load_articles()
	except IOError:
		dump_articles()
		articles = load_articles()
	
	articles = Paginator(articles, 30)
	requested_page = articles.page(page_number)
	
	return main_page.render(
		articles=requested_page,
		num_pages=articles.num_pages,
		page_num=page_number,
	)

t1 = Thread(target=dump_articles_per_sec)
t1.daemon = True
t1.start()

if __name__ == "__main__":	
	run(host="0.0.0.0", port="8080", server="gunicorn")

app = default_app()
