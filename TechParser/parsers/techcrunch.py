#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'techcrunch'

def get_articles():
	return parser.get_articles_from_rss('http://techcrunch.com/feed', SHORT_NAME)
