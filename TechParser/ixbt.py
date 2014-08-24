#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
import feedparser

def get_articles():
	res = feedparser.parse("http://www.ixbt.com/export/utf8/articles.rss")
	res = res["entries"]
	articles = [{'title': i['title'], 'link': i['link'], 'source': 'ixbt'}
		for i in res]
	
	return articles
