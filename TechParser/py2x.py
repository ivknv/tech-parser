#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	unicode__ = unicode
	unicode_ = lambda s: unicode(s, 'utf8')
except NameError:
	unicode_, unicode__ = str, str

try:
	chr = unichr
except NameError:
	chr = chr

try:
	range = xrange
except NameError:
	range = range

try:
	import htmlentitydefs
except ImportError:
	from html import entities as htmlentitydefs

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse

try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode

try:
	from itertools import zip_longest
except ImportError:
	from itertools import izip_longest as zip_longest

try:
	import cPickle as pickle
except ImportError:
	import pickle
