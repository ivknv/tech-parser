#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sqlite3
import pickle

try:
	import psycopg2
except ImportError:
	pass

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse

logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

r1 = re.compile(r"(?P<g1>\w+)n['\u2019]t", re.UNICODE)
r2 = re.compile(r"(?P<g1>\w+)['\u2019]s", re.UNICODE)
r3 = re.compile(r"(?P<g1>\w+)['\u2019]m", re.UNICODE)
r4 = re.compile(r"(?P<g1>\w+)['\u2019]re", re.UNICODE)
r5 = re.compile(r"(?P<g1>\w+)['\u2019]ve", re.UNICODE)
r6 = re.compile(r"(?P<g1>\w+)['\u2019]d", re.UNICODE)
r7 = re.compile(r"(?P<g1>\w+)['\u2019]ll", re.UNICODE)
r8 = re.compile(r"gonna", re.UNICODE)
r9 = re.compile(r"\W", re.UNICODE)

def get_similarity(pairs1, pairs2):
	len_all_pairs = len(pairs1) + len(pairs2)
	shrd = pairs1 & pairs2
	
	if len_all_pairs == 0:
		return 0.0
	
	return 2.0 * len(shrd) / len_all_pairs

def pairs_fromstring(s):
	return get_pairs(prepare_string(s))

def article_pairs(article):
	title_pairs = pairs_fromstring(article['title'])
	summary_prepared = prepare_string(article['summary'])
	if len(summary_prepared) > 30:
		return title_pairs and get_pairs(summary_prepared)
	
	return title_pairs

def find_similiar(articles, db='sqlite'):
	interesting_articles = get_interesting_articles(db)
	blacklist = get_blacklist(db)
	ignored_links = [i['link'] for i in blacklist]
	processed, scores = [], []
	interesting_links = [i['link']
		for i in interesting_articles]
	
	interesting_pairs = [article_pairs(i)
		for i in interesting_articles[:150]]
	ignored_pairs = [article_pairs(i)
		for i in blacklist[:150]]
	
	while len(interesting_pairs) > len(ignored_pairs):
		ignored_pairs.append(set())
	while len(ignored_pairs) > len(interesting_pairs):
		interesting_pairs.append(set())
	
	zipped = list(zip(interesting_pairs, ignored_pairs))
	
	for article in articles:
		if article['link'] in interesting_links or \
		article['link'] in ignored_links:
			continue
		
		score = 0.0
		
		pairs1 = article_pairs(article)
		
		for (pairs2, pairs3) in zipped:
			if pairs2:
				score += get_similarity(pairs1, pairs2)
			if pairs3:
				score -= get_similarity(pairs1, pairs3)
		
		processed.append(article)
		scores.append(score)
	
	return [[a, s] for (a, s) in zip(processed, scores)]

def prepare_string(s, exclude=["a", "an", "the", "is", "am", "there", "this",
		"are", "for", "that", "of", "to", "so", "in", "on", "off", "those",
		"these", "you", "he", "she", "they", "we", "out"]):
	s = s.strip().lower()
	s = r1.sub("\g<g1> not", s)
	s = r2.sub("\g<g1>", s)
	s = r3.sub("\g<g1> am", s)
	s = r4.sub("\g<g1> are", s)
	s = r5.sub("\g<g1> have", s)
	s = r6.sub("\g<g1> would", s)
	s = r7.sub("\g<g1> will", s)
	s = r8.sub("going to", s)
	words = r9.split(s)
	
	return [word for word in words if len(word) and word not in exclude]

def get_pairs(words):
	pairs = set()
	for word in words:
		pairs.update({word[i:i+2] for i in range(len(word))})
	return pairs

def get_interesting_articles(db='sqlite'):
	setup_db(db)
	connect, args, kwargs = which_db(db)
	con = connect(*args, **kwargs)
	cur = con.cursor()
	cur.execute('''SELECT title, link, summary, fromrss, icon, color, source
		FROM interesting_articles ORDER BY id DESC;''')
	res = cur.fetchall()
	con.close()
	return [{'title': x[0],
			'link': x[1],
			'summary': x[2],
			'fromrss': x[3],
			'icon': x[4],
			'color': x[5],
			'source': x[6]} for x in res]

def get_blacklist(db='sqlite'):
	setup_db(db)
	connect, args, kwargs = which_db(db)
	con = connect(*args, **kwargs)
	cur = con.cursor()
	cur.execute('''SELECT title, link, summary, fromrss, icon, color, source
		FROM blacklist ORDER BY id DESC;''')
	res = cur.fetchall()
	con.close()
	return [{'title': x[0],
			'link': x[1],
			'summary': x[2],
			'fromrss': x[3],
			'icon': x[4],
			'color': x[5],
			'source': x[6]} for x in res]

def add_article(addr, db='sqlite'):
	f = open(os.path.join(logdir, "articles_dumped"), 'rb')
	dumped = f.read()
	f.close()
	
	articles = pickle.loads(dumped)
	
	for article in articles:
		if article[0]['link'] == addr:
			add_to_interesting(article, db)
			break

def add_to_interesting(article, db='sqlite'):
	setup_db(db)
	
	connect, args, kwargs = which_db(db)
	
	if db == 'sqlite':
		IntegrityError = sqlite3.IntegrityError
	else:
		try:
			IntegrityError = psycopg2.IntegrityError
		except NameError:
			IntegrityError = sqlite3.IntegrityError
	
	con = connect(*args, **kwargs)
	cur = con.cursor()
	cur.execute('SELECT count(link) FROM interesting_articles;')
	if cur.fetchone()[0] > 1000:
		cur.execute("""DELETE FROM interesting_articles
			WHERE id = (SELECT MIN(id) FROM interesting_articles);""")
	sqlite_code = """INSERT INTO
			interesting_articles(title, link, summary, fromrss, icon, color, source)
				VALUES(?, ?, ?, ?, ?, ?, ?);"""
	postgres_code = """INSERT INTO
			interesting_articles(title, link, summary, fromrss, icon, color, source)
				VALUES(%s, %s, %s, %s, %s, %s, %s);"""
	
	if db == 'sqlite':
		code = sqlite_code
	else:
		code = postgres_code
	
	try:
		title = article[0]['title']
		link = article[0]['link']
		summary = article[0]['summary']
		source = article[0]['source']
		fromrss = article[0].get('fromrss', 0)
		icon = article[0].get('icon', '')
		color = article[0].get('color', '#000')
		
		cur.execute(code, (title, link, summary, fromrss, icon, color, source))
		con.commit()
	except IntegrityError:
		pass
	
	con.close()

def add_article_to_blacklist(addr, db='sqlite'):
	f = open(os.path.join(logdir, "articles_dumped"), 'rb')
	dumped = f.read()
	f.close()
	
	articles = pickle.loads(dumped)
	
	for article in articles:
		if article[0]['link'] == addr:
			f = open(os.path.join(logdir, "articles_dumped"), 'wb')
			add_to_blacklist(article, db)
			articles.remove(article)
			f.write(pickle.dumps(articles))
			f.close()
			break

def add_to_blacklist(article, db='sqlite'):
	setup_db(db)
	
	connect, args, kwargs = which_db(db)
	
	if db == 'sqlite':
		IntegrityError = sqlite3.IntegrityError
	else:
		try:
			IntegrityError = psycopg2.IntegrityError
		except NameError:
			IntegrityError = sqlite3.IntegrityError
	
	con = connect(*args, **kwargs)
	cur = con.cursor()

	sqlite_code = """INSERT INTO
			blacklist(title, link, summary, fromrss, icon, color, source)
				VALUES(?, ?, ?, ?, ?, ?, ?);"""
	postgres_code = """INSERT INTO
			blacklist(title, link, summary, fromrss, icon, color, source)
				VALUES(%s, %s, %s, %s, %s, %s, %s);"""
	
	if db == 'sqlite':
		code = sqlite_code
	else:
		code = postgres_code
	
	try:
		title = article[0]['title']
		link = article[0]['link']
		summary = article[0]['summary']
		source = article[0]['source']
		fromrss = article[0].get('fromrss', 0)
		icon = article[0].get('icon', '')
		color = article[0].get('color', '#000')
		cur.execute(code, (title, link, summary, fromrss, icon, color, source))
		con.commit()
	except IntegrityError:
		pass
	
	con.close()

def remove_from_history(link, db='sqlite'):
	setup_db(db)
	
	connect, args, kwargs = which_db(db)
	
	con = connect(*args, **kwargs)
	cur = con.cursor()
	
	sqlite_code = 'DELETE FROM interesting_articles WHERE link=?;'
	postgres_code = 'DELETE FROM interesting_articles WHERE link=%s;'
	
	code = postgres_code if db == 'postgresql' else sqlite_code
	
	cur.execute(code, (link,))
	con.commit()
	con.close()

def remove_from_blacklist(link, db='sqlite'):
	setup_db(db)
	
	connect, args, kwargs = which_db(db)
	
	con = connect(*args, **kwargs)
	cur = con.cursor()
	
	sqlite_code = 'DELETE FROM blacklist WHERE link=?;'
	postgres_code = 'DELETE FROM blacklist WHERE link=%s;'
	
	code = postgres_code if db == 'postgresql' else sqlite_code
	
	cur.execute(code, (link,))
	con.commit()
	con.close()

def setup_db(db='sqlite'):
	connect, args, kwargs = which_db(db)
	
	con = connect(*args, **kwargs)
	cur = con.cursor()
	sqlite_code = """CREATE TABLE IF NOT EXISTS interesting_articles
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT, link TEXT, summary TEXT, source TEXT,
				fromrss INTEGER, icon TEXT, color TEXT,
				UNIQUE(link));
		CREATE TABLE IF NOT EXISTS blacklist
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
				fromrss INTEGER, icon TEXT, color TEXT,
				title TEXT, link TEXT, summary TEXT, source TEXT,
				UNIQUE(link))"""
	postgres_code = """CREATE TABLE IF NOT EXISTS interesting_articles
			(id SERIAL,	title TEXT, link TEXT, summary TEXT,
				fromrss INTEGER, icon TEXT, color TEXT,
				source TEXT, UNIQUE(link));
		CREATE TABLE IF NOT EXISTS blacklist
			(id SERIAL, title TEXT, link TEXT, summary TEXT,
				fromrss INTEGER, icon TEXT, color TEXT,
				source TEXT, UNIQUE(link))"""
	if db == 'sqlite':
		code = sqlite_code
	elif db == 'postgresql':
		code = postgres_code
	for statement in code.split(';'):
		cur.execute(statement)
	con.commit()
	con.close()

def which_db(db):
	if db == 'postgresql':
		try:
			connect = psycopg2.connect
			kwargs = parse_dburl()
			args = tuple()
		except NameError:
			connect = sqlite3.connect
			kwargs = {}
			args = (os.path.join(logdir, 'interesting.db'),)
	elif db == 'sqlite':
		connect = sqlite3.connect
		kwargs = {}
		args = (os.path.join(logdir, 'interesting.db'),)
	else:
		raise Exception('db must be sqlite or postgresql')
	
	return (connect, args, kwargs)

def parse_dburl(var='DATABASE_URL'):
	parsed = urlparse(os.environ.get(var, ''))
	
	return {'user': parsed.username,
			'password': parsed.password,
			'host': parsed.hostname,
			'port': parsed.port,
			'dbname': parsed.path[1:]}
