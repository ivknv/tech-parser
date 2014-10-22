#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles(start_page=1, end_page=2):
	return parser.get_articles_from_rss('http://droider.ru/feed/', 'droider')
