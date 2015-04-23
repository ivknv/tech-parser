#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'ixbt'

def get_articles():
	return parser.get_articles_from_rss(
		'http://www.ixbt.com/export/utf8/articles.rss', SHORT_NAME)
