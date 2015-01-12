#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import get_conf
from TechParser.py2x import pickle
from collections import OrderedDict
import json

if not get_conf.config:
	get_conf.set_config_auto()

get_conf.auto_fix_config()

class Config(object):
	def __init__(self, hide=False, **kwargs):
		self.sites_to_parse = kwargs.get('sites_to_parse')
		self.rss_feeds = kwargs.get('rss_feeds')
		self.filters = kwargs.get('filters')
		self.interesting_words = kwargs.get('interesting_words')
		self.boring_words = kwargs.get('boring_words')
		self.update_interval = kwargs.get('update_interval')
		self.db = kwargs.get('db')
		self.db_path_variable = kwargs.get('db_path_variable', 'DATABASE_URL')
		if not hide or not self.db_path_variable:
			try:
				self.db_path = kwargs['db_path']
			except KeyError:
				pass
		self.host = kwargs.get('host')
		self.port = kwargs.get('port')
		self.num_threads = kwargs.get('num_threads')
		self.server = kwargs.get('server')
		self.save_articles = kwargs.get('save_articles')
		self.archive_db_path_variable = kwargs.get('archive_db_path_variable', 'ARCHIVE_DATABASE_URL')
		if not hide or not self.archive_db_path_variable:
			try:
				self.archive_db_path = kwargs['archive_db_path']
			except KeyError:
				pass
		self.data_format = kwargs.get('data_format')
		self.password_variable = kwargs.get('password_variable', 'TechParser_PASSWORD')
		if not hide or not self.password_variable:
			try:
				self.password = kwargs['password']
			except KeyError:
				pass
		self.enable_pocket = kwargs.get('enable_pocket')
		
		get_conf.auto_fix_config(self)
	
	@staticmethod
	def from_module(module, hide=False):
		d = {}
		d['sites_to_parse'] = {k: {'module': v['module'].__name__,
			'kwargs': v['kwargs']}
			for k,v in module.sites_to_parse.items()}
		d['rss_feeds'] = module.rss_feeds
		d['filters'] = module.filters
		d['interesting_words'] = module.interesting_words
		d['boring_words'] = module.boring_words
		d['update_interval'] = module.update_interval
		d['db'] = module.db
		d['db_path_variable'] = module.db_path_variable
		if not hide or not d['db_path_variable']:
			d['db_path'] = module.db_path
		d['host'] = module.host
		d['port'] = module.port
		d['num_threads'] = module.num_threads
		d['server'] = module.server
		d['save_articles'] = module.save_articles
		d['archive_db_path_variable'] = module.archive_db_path_variable
		if not hide or not d['archive_db_path_variable']:
			d['archive_db_path'] = module.archive_db_path
		d['data_format'] = module.data_format
		d['password_variable'] = module.password_variable
		if not hide or not d['password_variable']:
			d['password'] = module.password
		d['enable_pocket'] = module.enable_pocket
		
		return Config(**d)

def check_format(func):
	def newfunc(*args, **kwargs):
		msg = "data_format should be either 'json' or 'pickle'"
		assert get_conf.config.data_format in {'pickle', 'json'}, msg
		return func(*args, **kwargs)
	
	return newfunc

@check_format
def dump_data(data):
	if get_conf.config.data_format == 'pickle':
		return pickle.dumps(data)
	else:
		return json.dumps(data)

@check_format
def load_data(dumped_data):
	if get_conf.config.data_format == 'pickle':
		return pickle.loads(dumped_data)
	else:
		return json.loads(dumped_data, object_pairs_hook=OrderedDict)

def config_to_json(config):
	return json.dumps(Config.from_module(config, hide=True).__dict__)

def config_from_json(json_str):
	return Config(**json.loads(json_str))

def dump_to_file(data, filename):
	mode = 'w'
	if get_conf.config.data_format == 'pickle':
		mode += 'b'
	with open(filename, mode) as f:
		f.write(dump_data(data))

def load_from_file(filename):
	mode = 'r'
	if get_conf.config.data_format == 'pickle':
		mode += 'b'
	with open(filename, mode) as f:
		return load_data(f.read())
