#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'engadget'

def get_articles():
	return parser.get_articles_from_rss('http://engadget.com/rss.xml', SHORT_NAME)
