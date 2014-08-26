#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sqlite3
import pickle

logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

def get_words(s):
	words = prepare_string(s)
	
	return [word for word in words if word]

def get_similarity(article1, article2, split=get_words):
	parts1 = split(article1['title'])
	parts2 = split(article2['title'])
	
	len_all_parts = len(parts1) + len(parts2)
	shrd = []
	for part in parts1:
		if part in parts2:
			if shrd.count(part) < min(parts1.count(part), parts2.count(part)):
				shrd.append(part)
	
	return 2.0 * len(shrd) / len_all_parts

def find_similiar(articles):
	interesting_articles = get_interesting_articles()
	similiar_articles = []
	
	for article in articles:
		if article in interesting_articles:
			similiar_articles.append([article, 0.0])
			continue
		
		score = 0.0
		for interesting_article in interesting_articles:
			score += get_similarity(article, interesting_article, get_pairs)
		
#		if [article, average] not in similiar_articles:
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

def get_pairs(s):
	s = " ".join(prepare_string(s))
	return [p for p in [s[i:i+2] for i in range(len(s))] if p.count(" ") < 2]

def get_interesting_articles():
	setup_db()
	con = sqlite3.connect(os.path.join(logdir, 'interesting.db'))
	cur = con.cursor()
	cur.execute('SELECT * FROM interesting_articles;')
	res = cur.fetchall()
	return [{'title': x[1],
			'link': x[2],
			'source': x[3]} for x in res]

def add_article(addr):
	f = open(os.path.join(logdir, "articles_dumped"), 'rb')
	dumped = f.read()
	f.close()
	
	articles = pickle.loads(dumped)
	
	for article in articles:
		if article[0]['link'] == addr:
			break
	
	add_to_interesting(article)

def add_to_interesting(article):
	setup_db()
	con = sqlite3.connect(os.path.join(logdir, 'interesting.db'))
	cur = con.cursor()
	cur.execute('SELECT count(link) from interesting_articles;')
	if cur.fetchone()[0] > 150:
		cur.execute("""DELETE FROM interesting_articles
			WHERE id = (SELECT MIN(id) FROM interesting_articles);""")
	try:
		cur.execute("""INSERT INTO
			interesting_articles(title, link, source) VALUES(?, ?, ?);""",
			(article[0]['title'], article[0]['link'], article[0]['source']))
		con.commit()
	except sqlite3.IntegrityError:
		pass
	con.close()

def setup_db():
	con = sqlite3.connect(os.path.join(logdir, 'interesting.db'))
	cur = con.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS interesting_articles
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT, link TEXT, source TEXT, UNIQUE(link));""")
	con.commit()
	con.close()
