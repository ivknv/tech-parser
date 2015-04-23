#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser.parser import get_articles_from_rss

SHORT_NAME = 'recode'

def get_articles():
	return get_articles_from_rss('http://recode.net/feed/', SHORT_NAME)
