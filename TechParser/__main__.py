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

from TechParser import recommend, parser

try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

sys.path.append(os.path.expanduser("~/.tech-parser"))

try:
	import user_parser_config as config
except ImportError:
	import TechParser.parser_config as config

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

liked = recommend.get_interesting_articles(db=config.db)
disliked = recommend.get_blacklist(db=config.db)
liked_links = [i['link'] for i in liked]
disliked_links = [i['link'] for i in disliked]

def encoded_dict(in_dict):
	out_dict = {}
	for k, v in in_dict.items():
		if isinstance(v, unicode_):
			v = v.encode('utf8')
		elif isinstance(v, str):
			# Must be encoded in UTF-8
			v.decode('utf8')
		out_dict[k] = v
	return out_dict

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
	if n.endswith("1") and not n.endswith("11"):
		return s
	else:
		return s + "s"

class State(object):
	def __init__(self):
		self.progress = 0.0

def show_progress(s, state):
	progress = round(state.progress, 2)
	return "\033[0;32m[{}%]\033[0m ".format(progress)+s

def parse_site(queue, articles, state):
	while queue:
		site = queue.pop()
		s = "Got {} {} from {}"
		
		if site not in config.sites_to_parse:
			d = config.rss_feeds[site]
		else:
			d = config.sites_to_parse[site]
		
		log(show_progress("Parsing articles from {}".format(site), state))
		
		if 'module' not in d:
			url = d['url']
			short_name = d['short-name']
			icon = d['icon']
			color = d['color']
			if not len(color):
				color = '#FFF'
			if not len(icon):
				icon = 'about:blank'
			
			try:
				new_articles = parser.parse_rss(url, short_name, icon, color)
				articles += new_articles
				state.progress += 100.0 / (len(config.sites_to_parse) + len(config.rss_feeds))
				log(show_progress(s.format(len(new_articles),
					simple_plural(len(new_articles), 'article'), site), state))
			except Exception as error:
				log('Fail')
				log(str(error), f=sys.stderr)
		else:
			module = d["module"]
			kwargs = d["kwargs"]
			
			try:
				found = module.get_articles(**kwargs)
				articles += found
				state.progress += 100.0 / (len(config.sites_to_parse) + len(config.rss_feeds))
				log(show_progress(s.format(len(found),
					simple_plural(len(new_articles), 'article'), site), state))
			except Exception as error:
				log("Failed to parse articles from {}".format(site))
				log(str(error), f=sys.stderr)

def dump_articles():
	"""Dump articles to ~/.tech-parser/articles_dumped"""
	
	articles = []
	
	state = State()
	
	main_queue = [i for i in config.sites_to_parse]
	main_queue += [i for i in config.rss_feeds]
	
	s = "\033[0;32m[{}%]\033[0m Parsing articles from {}... "
	
	threads = []
	
	for i in range(config.num_threads):
		threads.append(Thread(target=parse_site, args=(main_queue,articles,state)))
	
	for thread in threads:
		thread.start()
	
	for thread in threads:
		thread.join()
	
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
	
	log("Ranking articles...")
	num = len(recommend.get_interesting_articles(db=config.db))
	num += len(recommend.get_blacklist(db=config.db))
	if num >= 20:
		articles = recommend.find_similiar(articles, db=config.db)
		articles.sort(key=lambda x: x[1], reverse=True)
	else:
		articles = [[a, -1] for a in articles]
	
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
	
	return articles

@route('/static/<filename:path>')
def serve_static(filename):
	"""Serve static files"""
	
	return static_file(filename, root=static_dir_path)

@route('/go/<addr:path>')
def go_to_url(addr):
	recommend.add_article(addr, db=config.db)
	redirect(addr)

@route('/histadd/<addr:path>')
def add_to_history(addr):
	global liked, disliked, liked_links, disliked_links
	
	recommend.add_article(addr, db=config.db)
	liked = recommend.get_interesting_articles(db=config.db)
	disliked = recommend.get_blacklist(db=config.db)
	liked_links = [i['link'] for i in liked]
	disliked_links = [i['link'] for i in disliked]

@route('/blacklistadd/<addr:path>')
def add_to_blacklist(addr):
	global liked, disliked, liked_links, disliked_links
	
	recommend.add_article_to_blacklist(addr, db=config.db)
	liked = recommend.get_interesting_articles(db=config.db)
	disliked = recommend.get_blacklist(db=config.db)
	liked_links = [i['link'] for i in liked]
	disliked_links = [i['link'] for i in disliked]

@route('/blacklistrm/<addr:path>')
def rm_from_blacklist(addr):
	recommend.remove_from_blacklist(addr, db=config.db)

@route('/histrm/<addr:path>')
def rm_from_history(addr):
	recommend.remove_from_history(addr, db=config.db)

@route('/history')
@route('/history/<page_number>')
def show_history(page_number=1):
	history_page = mylookup.get_template('history.html')
	q = request.GET.get('q', '')
	
	articles = recommend.get_interesting_articles(db=config.db)
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	if q:
		qs = q.lower().split()
		articles = filter(lambda x: has_words(qs, x), articles)
	
	articles = map(lambda x: replace_newlines(escape_link(x)), articles)
	
	all_articles = articles
	articles = split_into_pages(articles, 30)
	try:
		requested_page = articles[page_number-1]
	except IndexError:
		requested_page = []
	
	return history_page.render(articles=requested_page,
		num_pages=len(articles),
		page_num=page_number,
		q=q,
		all_articles=all_articles,)

@route('/blacklist')
@route('/blacklist/<page_number>')
def show_blacklist(page_number=1):
	history_page = mylookup.get_template('blacklist.html')
	q = request.GET.get('q', '')
	
	articles = recommend.get_blacklist(db=config.db)
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	if q:
		qs = q.lower().split()
		articles = filter(lambda x: has_words(qs, x), articles)
	
	articles = map(lambda x: replace_newlines(escape_link(x)), articles)
	
	all_articles = articles
	articles = split_into_pages(articles, 30)
	try:
		requested_page = articles[page_number-1]
	except IndexError:
		requested_page = []
	
	return history_page.render(articles=requested_page,
		num_pages=len(articles),
		page_num=page_number,
		q=q,
		all_articles=all_articles)


def has_words(qs, article):
	"""Check if article title contains words:"""
	
	title = article['title'].lower()
	
	for i in qs:
		if i not in title:
			return False
	return True

def escape_link(article):
	"""Escape HTML tags, etc."""
	
	new_article = {}
	new_article.update(article)
	new_article['original_link'] = new_article['link']
	
	new_article['link'] = urlencode(encoded_dict({'': new_article['link']}))[1:]
	return new_article

def set_liked(articles):
	for article in articles:
		article['liked'] = article['original_link'] in liked_links
		article['disliked'] = article['original_link'] in disliked_links

def replace_newlines(article):
	new_article = {}
	new_article.update(article)
	new_article['summary'] = new_article['summary'].replace('\n', '<br/>')
	
	return new_article

@route("/")
@route("/<page_number>")
def article_list(page_number=1):
	"""Show list of articles | Search for articles"""
	
	main_page = mylookup.get_template("articles.html")
	q = request.GET.get('q', '')
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	try:
		articles = load_articles()
	except IOError:
		dump_articles()
		articles = load_articles()
	
	articles = filter_articles(articles)
	if q:
		qs = q.lower().split()
		articles = filter(lambda x: has_words(qs, x[0]), articles)
	
	articles = map(lambda x: replace_newlines(escape_link(x[0])), articles)
	all_articles = articles
	articles = split_into_pages(articles, 30)
	try:
		requested_page = articles[page_number-1]
		set_liked(requested_page)
	except IndexError:
		requested_page = []
	
	return main_page.render(articles=requested_page,
		num_pages=len(articles),
		page_num=page_number,
		q=q,
		all_articles=all_articles,)

class ParserDaemon(Daemon):
	def __init__(self):
		pidfile = os.path.join(logdir, "tech-parser.pid")
		so = open(os.path.join(logdir, "output.log"), "a+")
		se = open(os.path.join(logdir, "error.log"), "a+")
		if os.stat(so.name).st_size > 102400:
			so.truncate()
		if os.stat(se.name).st_size > 102400:
			se.truncate()
		
		super(ParserDaemon, self).__init__(pidfile, stdout=so, stderr=se)
	
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
	run(host=host, port=port, server=config.server)

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
	
	if args.action:
		if args.action[0] == "run":
			if len(args.action) == 1:
				addr = config.host + ":" + config.port
			else:
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
else:
	app = default_app()
