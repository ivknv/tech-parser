#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from mako.lookup import TemplateLookup
from bottle import route, run, static_file, request
from collections import OrderedDict

from TechParser import get_conf, recommend, save
from TechParser.py2x import unicode_, unicode__, range, urlencode, pickle

module_path = os.path.dirname(os.path.realpath(__file__))
template_dir_path = os.path.join(module_path, "templates")
static_dir_path = os.path.join(module_path, "static")
logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

mylookup = TemplateLookup(directories=template_dir_path,
	default_filters=["decode.utf8"],
	input_encoding="utf-8", output_encoding="utf-8")

liked = []
disliked = []
liked_links = []
disliked_links = []

def encoded_dict(in_dict):
	out_dict = {}
	for k, v in in_dict.items():
		if isinstance(v, unicode__):
			v = v.encode('utf8')
		elif isinstance(v, str):
			# Must be encoded in UTF-8
			v.decode('utf8')
		out_dict[k] = v
	return out_dict

def remove_tags(s):
	return recommend.r0.sub('', s)

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
		
		i += 1
	
	return pages

def filter_articles(articles):
	"""Filter articles"""
	
	config = get_conf.config
	
	articles_filtered = OrderedDict()
	
	for article in articles.values():
		passing = True
		
		words_len = len(config.filters["All"]["or"])
		title = article["title"].lower()
		
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
			articles_filtered[article['link']] = article
	
	return articles_filtered

def load_articles(filename="articles_dumped"):
	"""Load articles from ~/.tech-parser/<filename>"""
	
	try:
		return save.load_from_file(os.path.join(logdir, filename))
	except (IOError, pickle.PickleError, TypeError):
		return []

@route('/static/<filename:path>')
def serve_static(filename):
	"""Serve static files"""
	
	return static_file(filename, root=static_dir_path)

def update_liked_disliked():
	global liked, disliked, liked_links, disliked_links

	config = get_conf.config
	
	liked = recommend.get_interesting_articles()
	disliked = recommend.get_blacklist()
	liked_links = [i['link'] for i in liked]
	disliked_links = [i['link'] for i in disliked]

@route('/histadd/<addr:path>')
def add_to_history(addr):
	
	recommend.add_article(addr)
	
	update_liked_disliked()
	
@route('/blacklistadd/<addr:path>')
def add_to_blacklist(addr):
	recommend.add_article_to_blacklist(addr)
	
	update_liked_disliked()

@route('/blacklistrm/<addr:path>')
def rm_from_blacklist(addr):
	recommend.remove_from_blacklist(addr)
	
	update_liked_disliked()

@route('/histrm/<addr:path>')
def rm_from_history(addr):
	recommend.remove_from_history(addr)
	
	update_liked_disliked()

@route('/history')
@route('/history/<page_number>')
def show_history(page_number=1):
	history_page = mylookup.get_template('history.html')
	q = unicode_(request.GET.get('q', ''))
	
	articles = recommend.get_interesting_articles()
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	if q:
		qs = q.lower().split()
		articles = filter(lambda x: has_words(qs, x), articles)
	
	articles = map(lambda x: escape_link(x), articles)
	
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

@route('/blacklist')
@route('/blacklist/<page_number>')
def show_blacklist(page_number=1):
	history_page = mylookup.get_template('blacklist.html')
	q = unicode_(request.GET.get('q', ''))
	
	articles = recommend.get_blacklist()
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	if q:
		qs = q.lower().split()
		articles = filter(lambda x: has_words(qs, x), articles)
	
	articles = map(lambda x: escape_link(x), articles)
	
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
	"""Check if article contains words"""
	
	title = remove_tags(unicode_(article['title']).lower())
	summary = remove_tags(unicode_(article['summary']).lower())
	
	for i in qs:
		if i not in title and i not in summary:
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

@route("/")
@route("/<page_number>")
def article_list(page_number=1):
	"""Show list of articles | Search for articles"""
	
	main_page = mylookup.get_template("articles.html")
	q = unicode_(request.GET.get('q', ''))
	
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
		articles = filter(lambda x: has_words(qs, x), articles.values())
		articles = map(lambda x: escape_link(x), articles)
	else:
		articles = map(lambda x: escape_link(x), articles.values())
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
