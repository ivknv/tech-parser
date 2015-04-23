#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'maketecheasier'

def get_articles():	
	return parser.get_articles_from_rss("http://www.maketecheasier.com/feed",
		SHORT_NAME)
