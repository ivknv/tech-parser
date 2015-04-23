#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

SHORT_NAME = 'slashdot'

def get_articles():
	return parser.get_articles_from_rss('http://rss.slashdot.org/Slashdot/slashdot',
		SHORT_NAME, False)
