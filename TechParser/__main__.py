#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle

import pickle

import os, sys, re

from grab.error import GrabError

from time import time, sleep

from threading import Thread

from mako.lookup import TemplateLookup

from bottle import route, run, static_file, default_app, redirect, request

from Daemo import Daemon

import argparse

import sqlite3

from TechParser import recommend

sys.path.append(os.path.expanduser("~/.tech-parser"))

running_as_daemon = False

module_path = os.path.dirname(os.path.realpath(__file__))
template_dir_path = os.path.join(module_path, "templates")
static_dir_path = os.path.join(module_path, "static")
logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

if not os.path.exists(logdir):
	os.mkdir(logdir)

if not os.path.exists(os.path.join(logdir, "__init__.py")):
	open(os.path.join(logdir, "__init__.py"), "w").close()

if not os.path.exists(os.path.join(logdir, "user_parser_config.py")):
	f = open(os.path.join(logdir, "user_parser_config.py"), "w")
	default_config = open(os.path.join(module_path, "parser_config.py"))
	f.write(default_config.read())
	default_config.close()
	f.close()

mylookup = TemplateLookup(directories=template_dir_path,
		default_filters=["decode.utf8"],
		input_encoding="utf-8", output_encoding="utf-8")

def setup_db():
	"""Setup archive database"""
	
	con = sqlite3.connect(os.path.join(logdir, "archive.db"))
	cur = con.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS articles
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT, link TEXT, source TEXT, UNIQUE(link));""")
	con.commit()
	con.close()

def log(text, f=sys.stdout, add_newline=True, clear_str=False,
	ignore_daemon=False):
	
	if add_newline:
		text += "\n"
	
	if (clear_str or running_as_daemon) and not ignore_daemon:
		text = re.sub(r"\033\[(\d+|\d+;\d+)m", "", text)
	
	f.write(text)
	f.flush()

def split_into_pages(articles, n=30):
	"""Split list into pages"""
	
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

def simple_plural(n, s):
	n = str(n)
	if n.endswith("1"):
		return s
	else:
		return s + "s"

def dump_articles():
	"""Dump articles to ~/.tech-parser/articles_dumped"""
	
	articles = []
	
	counter = 0
	completed = 0
	
	for site in config.sites_to_parse:
		
		s = "\033[0;32m[{}%]\033[0m Parsing articles from {}... "
		
		log(s.format(completed, site), add_newline=False)
		
		module = config.sites_to_parse[site]["module"]
		kwargs = config.sites_to_parse[site]["kwargs"]
		
		try:
			before = len(articles)
			articles += module.get_articles(**kwargs)
			after = len(articles)
			difference = after - before
			log("Found %d %s" %(difference,
				simple_plural(difference, "article")))
		except GrabError as error:
			log("Fail")
			log(str(error), f=sys.stderr)
		
		counter += 1
		completed = round(100.0 / len(config.sites_to_parse) * counter, 1)
	
	log("\033[0;32m[{}%]\033[0m".format(completed))
	
	log("Total articles: %d" %(len(articles)))
	
	if config.save_articles:
		log("Saving articles to archive...")
		
		setup_db()
		con = sqlite3.connect(os.path.join(logdir, "archive.db"))
		cur = con.cursor()
		
		for article in articles:
			title = article["title"]
			link = article["link"]
			source = article["source"]
			
			try:
				cur.execute("""INSERT INTO articles(title, link, source)
					values(?, ?, ?);""", (title, link, source))
			except sqlite3.IntegrityError:
				pass
		
		con.commit()
		con.close()
	
	log("Shuffling articles...")
	
	shuffle(articles)
	articles = recommend.find_similiar(articles)
	articles.sort(key=lambda x: x[1], reverse=True)
	
	log("Dumping data to file: articles_dumped...")
	
	dumped = pickle.dumps(articles)
	path = os.path.join(os.path.expanduser("~"), ".tech-parser")
	path = os.path.join(path, "articles_dumped")
	f = open(path, "wb")
	f.write(dumped)
	f.close()
	
	log("Done!")

def dump_articles_per(s):
	"""Dump articles per S seconds"""
	
	while True:
		if int(time()) % s == 0:
			dump_articles()
		sleep(1)

def filter_articles(articles):
	"""Filter articles"""
	
	articles_filtered = []
	
	for article in articles:
		passing = True
		
		words_len = len(config.filters["All"]["or"])
		title = article[0]["title"].lower()
		
		for word in config.filters["All"]["or"]:
			if word.lower() in title:
				passing = True
				break
			else:
				words_len -= 1
			
			if words_len == 0:
				passing = False
				
		if passing:
			for word in config.filters["All"]["not"]:
				if word.lower() in title:
					passing = False
					break
		if passing:	
			for word in config.filters["All"]["has"]:
				if word.lower() not in title:
					passing = False
					break	
		if passing:
			articles_filtered.append(article)
	
	return articles_filtered

def load_articles():
	"""Load articles from ~/.tech-parser/articles_dumped"""
	
	log("Reading articles from file: articles_dumped...")
	f = open(os.path.join(logdir, "articles_dumped"), 'rb')
	dumped = f.read()
	f.close()
	
	articles = pickle.loads(dumped)
	
	log("Done!")
	sys.stdout.write("Done!\n")
	sys.stdout.flush()
	
	return articles

@route('/static/<filename:path>')
def serve_static(filename):
	"""Serve static files"""
	
	return static_file(filename, root=static_dir_path)

@route('/go/<addr:path>')
def go_to_url(addr):
	recommend.add_article(addr)
	redirect(addr)

def has_words(qs, article):
	"""Check if article title contains words:"""
	
	title = article[0]['title'].lower()
	
	for i in qs:
		if i not in title:
			return False
	return True

def escape_titles(articles):
	"""Escape HTML tags, etc."""
	
	new_articles = []
	
	for article in articles:
		article[0]['title'] = article[0]['title'].replace('&', '&amp;')
		article[0]['title'] = article[0]['title'].replace('<', '&lt;')
		article[0]['title'] = article[0]['title'].replace('>', '&gt;')
		article[0]['title'] = article[0]['title'].replace('"', '&quot;')
		new_articles.append(article)
	
	return new_articles

@route("/")
@route("/<page_number>")
def article_list(page_number=1):
	"""Show list of articles | Search for articles"""
	
	main_page = mylookup.get_template("articles.html")
	q = request.GET.get('q', '').lower()
	
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
	if q:
		qs = q.split()
		articles = filter(lambda x: has_words(qs, x), articles)
	
	articles = escape_titles(articles)
	articles = split_into_pages(articles, 30)
	try:
		requested_page = articles[page_number-1]
	except IndexError:
		requested_page = []
	
	return main_page.render(articles=requested_page,
		num_pages=len(articles),
		page_num=page_number,
		q=q)

class ParserDaemon(Daemon):
	def __init__(self):
		pidfile = os.path.join(logdir, "tech-parser.pid")
		so = open(os.path.join(logdir, "output.log"), "a+")
		se = open(os.path.join(logdir, "error.log"), "a+")
		if os.stat(so.name).st_size > 102400:
			so.truncate()
		if os.stat(se.name).st_size > 102400:
			se.truncate()
		
		super(ParserDaemon, self).__init__(pidfile, True, stdout=so, stderr=se)
	
	def onStart(self):
		t1 = Thread(target=dump_articles_per, args=(config.update_interval,))
		t1.daemon = True
		t1.start()
		run(host=config.host, port=config.port, server=config.server)

def is_hostname(hostname):
	if len(hostname) > 255:
		return False
	if hostname[-1] == ".":
		hostname = hostname[:-1]
	allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
	return all(allowed.match(x) for x in hostname.split("."))

def run_server(host, port):
	t1 = Thread(target=dump_articles_per, args=(config.update_interval,))
	t1.daemon = True
	t1.start()
	run(host=host, port=port)

if __name__ == "__main__":
	parser_daemon = ParserDaemon()
	running_as_daemon = True
	
	arg_parser = argparse.ArgumentParser(description="""\
Article parser.
Available commands: start|stop|restart|update|run HOST:PORT""")
	
	arg_parser.add_argument("action", nargs="+",
		action="store", default=[], help="Action to run")
	arg_parser.add_argument("--config", help="Path to configuration")
	
	args = arg_parser.parse_args()
	
	if args.config:
		import imp
		config = imp.load_source('config', args.config)
	else:
		try:
			import user_parser_config as config
		except ImportError:
			import TechParser.parser_config as config
	
	if args.action:
		if args.action[0] == "run":
			addr = args.action[1]
			if not ":" in addr:
				addr += ":80"
			elif addr.endswith(":"):
				addr += "80"
		
			host, port = addr.split(":")
			is_host_correct = is_hostname(host)
			
			try:
				is_port_correct = int(port) <= 65535 and int(port) > 0
			except ValueError:
				is_port_correct = False
				
			if not is_host_correct:
				log("Incorrect hostname", f=sys.stderr)
				sys.exit(1)
			elif not is_port_correct:
				log("Incorrect port", f=sys.stderr)
				sys.exit(1)
			else:
				run_server(host, port)
		elif args.action[0] == "update":
			oldlog = log
			def log(*args, **kwargs):
				kwargs["ignore_daemon"] = True
				oldlog(*args, **kwargs)
			dump_articles()
		elif args.action[0] == "start":
			parser_daemon.start()
		elif args.action[0] == "stop":
			parser_daemon.stop()
		elif args.action[0] == "restart":
			parser_daemon.restart()
else:
	app = default_app()
