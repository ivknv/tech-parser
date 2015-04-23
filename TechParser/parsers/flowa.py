#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'flowa'

def get_articles():
	return parser.get_articles_from_rss('http://flowa.fi/rss.xml', SHORT_NAME)
