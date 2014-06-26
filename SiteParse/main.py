#!/usr/bin/env python
# -*- coding: utf-8 -*-

import habrahabr
import engadget
import slashdot
import venturebeat
import gizmodo
import techcrunch
import readwrite
import techrepublic

from random import shuffle

import pickle

from grab.error import GrabError

from time import time, sleep

from threading import Thread

from django.core.paginator import Paginator

from mako.template import Template
from mako.lookup import TemplateLookup

from bottle import route, run, static_file, default_app

mylookup = TemplateLookup(directories="templates", default_filters=["decode.utf8"], input_encoding="utf-8", output_encoding="utf-8")

articles = []

def dump_articles():
	
	tasks = {
		"Habrahabr": {
			"module": habrahabr,
			"kwargs": {}
		},
		
		"VentureBeat": {
			"module": venturebeat,
			"kwargs": {}
		},
		
		"Engadget": {
			"module": engadget,
			"kwargs": {}
		},
		
		"Slashdot": {
			"module": slashdot,
			"kwargs": {"end_page": 3}
		},
		
		"Gizmodo": {
			"module": gizmodo,
			"kwargs": {}
		},
		
		"TechCrunch": {
			"module": techcrunch,
			"kwargs": {}
		},
		
		"Read/Write Web": {
			"module": readwrite,
			"kwargs": {}
		},
		
		"Tech Republic": {
			"module": techrepublic,
			"kwargs": {}
		}
	}
	
	articles = []
	
	counter = 0
	completed = 0
	
	for task in tasks:
		print("\033[0;32m[{}%]\033[0m Parsing articles from {}...".format(completed, task))
		
		module = tasks[task]["module"]
		kwargs = tasks[task]["kwargs"]
		
		try:
			articles += module.get_articles(**kwargs)
		except GrabError as error:
			print(error)
		
		counter += 1
		completed = round(100.0 / 8.0 * counter, 1)
	
	print("\033[0;32m[{}%]\033[0m".format(completed))
		
	print("Shuffling articles...")
	
	shuffle(articles)
	
	print("Dumping data to file: articles_dumped...")
	
	dumped = pickle.dumps(articles)
	f = open("articles_dumped", "w")
	f.write(dumped)
	f.close()
	
	print("Done!")

def dump_articles_per_sec(s=30*60):
	while True:
		if int(time()) % s == 0:
			dump_articles()
		sleep(1)

def load_articles():
	print("Reading articles from file: articles_dumped...")
	f = open("articles_dumped")
	dumped = f.read()
	f.close()
	
	articles = pickle.loads(dumped)
	
	print("Done!")
	
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
