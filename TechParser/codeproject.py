#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles(categories=['all']):
	articles = []
	cids = {'all': '1', 'android': '22', 'ios': '25', 'c++': '2',
		'c#': '3', 'web': '23'}
	if 'all' in categories:
		ids = [cids['all']]
	else:
		ids = [cids[cat] for cat in categories]
	
	urls = ['http://www.codeproject.com/WebServices/ArticleRSS.aspx?cat='+i
		for i in ids]
	
	for url in urls:
		parsed = parser.get_articles_from_rss(url, 'codeproject')
		for article in parsed:
			if not article in articles:
				articles.append(article)
	
	return articles
