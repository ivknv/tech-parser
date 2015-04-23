#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'techrepublic'

def get_articles():
	return parser.get_articles_from_rss(
		'http://www.techrepublic.com/rssfeeds/articles/latest/',
		SHORT_NAME)
