#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

SHORT_NAME = 'ittoolbox'

def get_articles():
    g = grab.Grab()
    g.config['connect_timeout'] = 15
    g.go("http://it.toolbox.com")
    
    css_path = ".tile .tileContent div:first-child .floatleft:nth-child(2) a"
    
    return parser.get_articles(g, css_path, css_path, SHORT_NAME)
