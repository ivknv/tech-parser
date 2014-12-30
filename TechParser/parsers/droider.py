#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import parser

def get_articles(*args, **kwargs):
	return parser.get_articles_from_rss('http://droider.ru/feed/', 'droider')
