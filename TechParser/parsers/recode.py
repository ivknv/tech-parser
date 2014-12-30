#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser.parser import remove_tags, cut_text

def get_articles():
	articles = []
	url = 'http://recode.net/feed/'
	res = feedparser.parse(url)
	
	for entry in res['entries']:
		if 'media_thumbnail' in entry:
			img_src = entry.media_thumbnail[0]['url']
			img = u'<img src="%s" />' %img_src
		else:
			img = ''
		articles.append({'title': entry['title'],
					'link': entry['link'],
					'source': 'recode',
					'summary': img +cut_text(remove_tags(entry['summary']))})
	
	return articles
