#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser.parser import remove_tags, cut_text

def get_articles():
	res = feedparser.parse("http://www.ixbt.com/export/utf8/articles.rss")
	res = res["entries"]
	articles = [{'title': i['title'],
				'link': i['link'],
				'source': 'ixbt',
				'summary': cut_text(remove_tags(i['summary']))}
		for i in res]
	
	return articles
