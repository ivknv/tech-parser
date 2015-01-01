#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import get_conf
from TechParser.py2x import pickle
from collections import OrderedDict
import json

if not get_conf.config:
	get_conf.set_config_auto()

get_conf.auto_fix_config()

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
