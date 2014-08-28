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

def get_similarity(article1, article2):
	pairs1 = get_pairs(prepare_string(article1['title']))
	pairs2 = get_pairs(prepare_string(article2['title']))
	
	len_all_pairs = len(pairs1) + len(pairs2)
	shrd = []
	for pair in pairs1:
		if pair in pairs2:
			if shrd.count(pair) < min(pairs1.count(pair), pairs2.count(pair)):
				shrd.append(pair)
	
	if len_all_pairs == 0:
		return 0.0
	
	return 2.0 * len(shrd) / len_all_pairs

def find_similiar(articles, db='sqlite'):
	interesting_articles = get_interesting_articles(db)
	similiar_articles = []
	interesting_links = [i['link']
		for i in interesting_articles]
	
	for article in articles:
		if article['link'] in interesting_links:
			continue
		
		score = 0.0
		for interesting_article in interesting_articles:
			score += get_similarity(article, interesting_article)
		
		if [article, score] not in similiar_articles:
			similiar_articles.append([article, score])
	
	return similiar_articles

def prepare_string(s, exclude=["a", "an", "the", "is", "am",
		"are", "for", "that", "of", "to", "so", "in", "on"]):
	s = s.strip().lower()
	r1 = re.compile(r"(?P<g1>\w+)n['\u2019]t", re.UNICODE)
	r2 = re.compile(r"(?P<g1>\w+)['\u2019]s", re.UNICODE)
	r3 = re.compile(r"(?P<g1>\w+)['\u2019]m", re.UNICODE)
	r4 = re.compile(r"(?P<g1>\w+)['\u2019]re", re.UNICODE)
	r5 = re.compile(r"(?P<g1>\w+)['\u2019]ve", re.UNICODE)
	r6 = re.compile(r"(?P<g1>\w+)['\u2019]d", re.UNICODE)
	r7 = re.compile(r"(?P<g1>\w+)['\u2019]ll", re.UNICODE)
	r8 = re.compile(r"gonna", re.UNICODE)
	s = r1.sub("\g<g1> not", s)
	s = r2.sub("\g<g1>", s)
	s = r3.sub("\g<g1> am", s)
	s = r4.sub("\g<g1> are", s)
	s = r5.sub("\g<g1> have", s)
	s = r6.sub("\g<g1> would", s)
	s = r7.sub("\g<g1> will", s)
	s = r8.sub("going to", s)
	words = re.split(r"\W", s)
	for word in exclude:
		while words.count(word) > 0:
			words.remove(word)
	
	return [word for word in words if len(word)]

def get_pairs(words):
	pairs = []
	for word in words:
		if len(word) == 1:
			pairs.append(word)
		else:
			pairs += [word[i:i+2] for i in range(len(word))]
	return pairs

def get_interesting_articles(db='sqlite'):
	setup_db(db)
	connect, args, kwargs = which_db(db)
	con = connect(*args, **kwargs)
	cur = con.cursor()
	cur.execute('SELECT * FROM interesting_articles;')
	res = cur.fetchall()
	con.close()
	return [{'title': x[1],
			'link': x[2],
			'summary': x[3],
			'source': x[4]} for x in res]

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
	if cur.fetchone()[0] > 150:
		cur.execute("""DELETE FROM interesting_articles
			WHERE id == (SELECT MIN(id) FROM interesting_articles);""")
	sqlite_code = """INSERT INTO
			interesting_articles(title, link, summary, source) VALUES(?, ?, ?, ?);"""
	postgres_code = """INSERT INTO
			interesting_articles(title, link, summary, source) VALUES(%s, %s, %s, %s);"""
	
	if db == 'sqlite':
		code = sqlite_code
	else:
		code = postgres_code
	
	try:
		cur.execute(code, (article[0]['title'], article[0]['link'],
			article[0]['summary'], article[0]['source']))
		con.commit()
	except IntegrityError:
		pass
	
	con.close()

def setup_db(db='sqlite'):
	connect, args, kwargs = which_db(db)
	
	con = connect(*args, **kwargs)
	cur = con.cursor()
	sqlite_code = """CREATE TABLE IF NOT EXISTS interesting_articles
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT, link TEXT, summary TEXT, source TEXT,
				UNIQUE(link));"""
	postgres_code = """CREATE TABLE IF NOT EXISTS interesting_articles
			(id SERIAL,	title TEXT, link TEXT, summary TEXT,
				source TEXT, UNIQUE(link));"""
	if db == 'sqlite':
		cur.execute(sqlite_code)
	elif db == 'postgresql':
		cur.execute(postgres_code)
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
