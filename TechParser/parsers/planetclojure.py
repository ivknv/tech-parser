#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser.parser import get_articles_from_rss

def get_articles():
    return get_articles_from_rss('http://planet.clojure.in/atom.xml', 'planetclojure')
