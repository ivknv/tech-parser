#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'androidcentral'

def get_articles():
	return parser.get_articles_from_rss('http://gizmodo.com/rss', SHORT_NAME)
