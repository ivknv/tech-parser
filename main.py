#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser_config import *

from random import shuffle

import pickle

import os

from grab.error import GrabError

from time import time, sleep

from threading import Thread

from mako.template import Template
from mako.lookup import TemplateLookup

from bottle import route, run, static_file, default_app

from Daemo import Daemon

mylookup = TemplateLookup(directories="templates", default_filters=["decode.utf8"], input_encoding="utf-8", output_encoding="utf-8")

articles = []

def split_into_pages(articles, n=30):
	pages = []
	i = 0
	
	for j in articles:
		if i >= n:
			i = 0
		
		if i == 0:
			pages.append([j])
		else:
			pages[-1].append(j)
		
		i+=1
	
	return pages

def dump_articles():
	
	articles = []
	
	counter = 0
	completed = 0
	
	for site in sites_to_parse:
		print("\033[0;32m[{}%]\033[0m Parsing articles from {}...".format(completed, site))
		
		module = sites_to_parse[site]["module"]
		kwargs = sites_to_parse[site]["kwargs"]
		
		try:
			articles += module.get_articles(**kwargs)
		except GrabError as error:
			print(error)
		
		counter += 1
		completed = round(100.0 / len(sites_to_parse) * counter, 1)
	
	print("\033[0;32m[{}%]\033[0m".format(completed))
		
	print("Shuffling articles...")
	
	shuffle(articles)
	
	print("Dumping data to file: articles_dumped...")
	
	dumped = pickle.dumps(articles)
	f = open("articles_dumped", "w")
	f.write(dumped)
	f.close()
	
	print("Done!")

def dump_articles_per_sec(s=update_interval):
	while True:
		if int(time()) % s == 0:
			dump_articles()
		sleep(1)

def filter_articles(articles):
	articles_filtered = []
	
	for article in articles:
		passing = True
		
		words_len = len(filters["All"]["or"])
		
		for word in filters["All"]["or"]:
			if word.lower() in article["title"].lower():
				passing = True
				break
			else:
				words_len -= 1
			
			if words_len == 0:
				passing = False
				
		if passing:
			for word in filters["All"]["not"]:
				if word.lower() in article["title"].lower():
					passing = False
					break
		if passing:	
			for word in filters["All"]["has"]:
				if word.lower() not in article["title"].lower():
					passing = False
					break	
		if passing:
			articles_filtered.append(article)
	
	return articles_filtered

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
	
	articles = filter_articles(articles)
	articles = split_into_pages(articles, 30)
	requested_page = articles[page_number]
	
	return main_page.render(
		articles=requested_page,
		num_pages=len(articles),
		page_num=page_number,
	)

class ParserDaemon(Daemon):
	def __init__(self):
		pidfile = os.path.expanduser("~/tech-parser.pid")
		
		super(ParserDaemon, self).__init__(pidfile, True)
		
		sys.stdout = open(os.devnull, "w")
		sys.stderr = open(os.devnull, "w")
	
	def onStart(self):
		t1 = Thread(target=dump_articles_per_sec)
		t1.daemon = True
		t1.start()
		run(host=host, port=port, server=server)

if __name__ == "__main__":
	import sys
	
	if len(sys.argv) == 1:
		print("usage: %s start|stop|restart" %sys.argv[0])
	else:
		command = sys.argv[1].lower()
		
		if command in ["start", "stop", "restart"]:
			parser_daemon = ParserDaemon()
		else:
			print("usage: %s start|stop|restart" %sys.argv[0])
		
		if command == "start":
			parser_daemon.start()
		elif command == "stop":
			parser_daemon.stop()
		elif command == "restart":
			parser_daemon.restart()
		elif command == "update":
			dump_articles()

else:
	app = default_app()
