#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp, os

logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

config = None

def get_default_config():
	return __import__('TechParser.parser_config').parser_config

def get_config(fname):
	return imp.load_source('parser_config', fname)

def set_config(parser_config):
	global config
	
	config = parser_config

def set_config_from_fname(fname):
	set_config(get_config(fname))

def set_default_config():
	set_config(get_default_config())

def set_config_from_logdir(fname):
	set_config_from_fname(os.path.join(logdir, fname))

def set_user_config():
	set_config_from_logdir('user_parser_config.py')

def set_config_auto():
	try:
		set_user_config()
	except IOError:
		set_default_config()

def setdefault(obj, attr, value=None):
	try:
		getattr(obj, attr)
	except AttributeError:
		setattr(obj, attr, value)

def auto_fix_config():
	setdefault(config, 'sites_to_parse', {})
	setdefault(config, 'rss_feeds', {})
	setdefault(config, 'interesting_words', set())
	setdefault(config, 'boring_words', set())
	setdefault(config, 'host', '0.0.0.0')
	setdefault(config, 'port', 8080)
	setdefault(config, 'num_threads', 2)
	setdefault(config, 'save_articles', False)
	setdefault(config, 'db', 'sqlite')
	setdefault(config, 'server', 'auto')
	setdefault(config, 'update_interval', 1800)
	setdefault(config, 'filters', {'All': {'has': [], 'or': [], 'not': []}})
