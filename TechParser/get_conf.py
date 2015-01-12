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

def auto_fix_config(conf=None):
	if conf is None:
		conf = config
	setdefault(conf, 'sites_to_parse', {})
	setdefault(conf, 'rss_feeds', {})
	setdefault(conf, 'interesting_words', set())
	setdefault(conf, 'boring_words', set())
	setdefault(conf, 'host', '0.0.0.0')
	setdefault(conf, 'port', 8080)
	setdefault(conf, 'num_threads', 2)
	setdefault(conf, 'save_articles', False)
	setdefault(conf, 'db', 'sqlite')
	setdefault(conf, 'server', 'auto')
	setdefault(conf, 'update_interval', 1800)
	setdefault(conf, 'filters', {'All': {'has': [], 'or': [], 'not': []}})
	setdefault(conf, 'archive_db_path_variable', '')
	setdefault(conf, 'archive_db_path',
		os.environ.get(conf.archive_db_path_variable, 'default'))
	setdefault(conf, 'db_path_variable', '')
	setdefault(conf, 'db_path', os.environ.get(conf.db_path_variable, ''))
	setdefault(conf, 'data_format', 'pickle')
	setdefault(conf, 'password_variable', '')
	setdefault(conf, 'password', os.environ.get(conf.password_variable, ''))
	setdefault(conf, 'enable_pocket', False)
