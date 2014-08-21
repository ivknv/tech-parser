#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sqlite3
import pickle

logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

def get_similarity(article1, article2):
	words1 = get_words(article1['title'])
	words2 = get_words(article2['title'])
	len_all_words = len(words1) + len(words2)
	len_shrd = len([word for word in words1 if word in words2])
	return 2.0 * len_shrd / len_all_words

def find_similiar(articles, sim=get_similarity):
	interesting_articles = get_interesting_articles()
	similiar_articles = []
	
	for article in articles:
		if article in interesting_articles:
			similiar_articles.append([article, 0.0])
			continue
		
		scores = []
		for interesting_article in interesting_articles:
			score = sim(article, interesting_article)
			scores.append(score)
		average = sum(scores) / len(scores)
		if [article, average] not in similiar_articles:
			similiar_articles.append([article, average])
	
	return similiar_articles

def get_words(s, exclude=["a", "an", "the"]):
	s = s.strip().lower()
	r1 = re.compile(r"(?P<g1>[a-zA-Z]+)n['\u2019]t", re.UNICODE)
	r2 = re.compile(r"(?P<g1>[a-zA-Z])['\u2019]s", re.UNICODE)
	r3 = re.compile(r"(?P<g1>[a-zA-Z])['\u2019]m", re.UNICODE)
	r4 = re.compile(r"(?P<g1>[a-zA-Z])['\u2019]re", re.UNICODE)
	r5 = re.compile(r"(?P<g1>[a-zA-Z])['\u2019]ve", re.UNICODE)
	r6 = re.compile(r"(?P<g1>[a-zA-Z])['\u2019]d", re.UNICODE)
	r7 = re.compile(u"[^А-Я^а-я^A-Z^a-z^ ]", re.UNICODE)
	s = r1.sub("\g<g1> not", s)
	s = r2.sub("\g<g1>", s)
	s = r3.sub("\g<g1> am", s)
	s = r4.sub("\g<g1> are", s)
	s = r5.sub("\g<g1> have", s)
	s = r6.sub("\g<g1> would", s)
	s = r7.sub("", s)
	
	words = s.split(" ")
	for word in exclude:
		try:
			words.remove(word)
		except ValueError:
			pass
	
	return words

def get_interesting_articles():
	con = sqlite3.connect(os.path.join(logdir, 'interesting.db'))
	cur = con.cursor()
	cur.execute('SELECT * FROM interesting_articles;')
	res = cur.fetchall()
	return [{'title': article[1],
			'link': article[2],
			'source': article[3]} for article in res]

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
