#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TechParser import parser

SHORT_NAME = 'venturebeat'

def get_articles():
	return parser.get_articles_from_rss("http://venturebeat.com/feed",
		SHORT_NAME)
