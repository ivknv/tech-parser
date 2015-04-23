#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'topdesignmagazine'

def get_articles():
	return parser.get_articles_from_rss(
		'http://feeds.feedburner.com/topdesignmagazine', SHORT_NAME)
