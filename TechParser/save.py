#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import get_conf
from TechParser.py2x import pickle
import json

if not get_conf.config:
	get_conf.set_config_auto()

get_conf.auto_fix_config()

open_file = open

def jsonopen(filename, mode):
	return open(filename, mode)

def pickleopen(filename, mode):
	return open(filename, mode + 'b')

def set_open_file():
	global open_file
	
	if get_conf.config.data_format == 'pickle':
		open_file = pickleopen
	else:
		open_file = jsonopen

def get_module():
	msg = "data_format should be either 'json' or 'pickle'"
	assert get_conf.config.data_format in {'pickle', 'json'}, msg
	if get_conf.config.data_format == 'pickle':
		open_file = pickleopen
		return pickle
	else:
		open_file = jsonopen
		return json

def dump_data(data):
	return get_module().dumps(data)

def load_data(dumped_data):
	return get_module().loads(dumped_data)

def dump_to_file(data, filename):
	set_open_file()
	
	with open_file(filename, 'w') as f:
		f.write(dump_data(data))

def load_from_file(filename):
	set_open_file()
	
	with open_file(filename, 'r') as f:
		return load_data(f.read())
