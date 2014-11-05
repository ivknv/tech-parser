#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles(categories=['all']):
	urls = {'articles': 'b_text', 'news': 'b_news', 'all': '1',
		'games': 'games', 'programs': 'progs', 'themes': 'themes',
		'questions': 'b_questions', 'main_page': '1/?approved'}
	
	if 'all' in categories:
		selected_urls = [urls['all']]
	else:
		selected_urls = [urls[i] for i in categories if i in categories]
	
	articles = []
	append = articles.append #OPTIMISATION
	
	for url in selected_urls:
		url_ = 'http://trashbox.ru/feed_topics/{0}'.format(url)
		for article in parser.get_articles_from_rss(url_, 'trashbox'):
			if article not in articles:
				append(article)

	return articles
