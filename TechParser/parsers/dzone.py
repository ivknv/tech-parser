#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'dzone'

def get_articles():
	return parser.get_articles_from_rss('http://feeds.dzone.com/dzone/frontpage',
		SHORT_NAME)
