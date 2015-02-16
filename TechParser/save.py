#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import get_conf
from TechParser.py2x import pickle
from collections import OrderedDict
import json
import os
from TechParser.db_functions import save_articles, select_all_articles

if not get_conf.config:
    get_conf.set_config_auto()

get_conf.auto_fix_config()

def check_format(func):
    def newfunc(*args, **kwargs):
        msg = "data_format should be 'json', 'pickle' or 'db'"
        assert get_conf.config.data_format in {'pickle', 'json', 'db'}, msg
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
    return json.dumps(get_conf.Config.from_module(config, hide=True).__dict__, ensure_ascii=False, indent=4, sort_keys=True)

def write_config(config, filename=os.path.join(get_conf.logdir, 'user_parser_config.json')):
    with open(filename, 'w') as f:
        f.write(config_to_json(config))

def dump_somewhere(data, filename=None):
    mode = 'w'
    if get_conf.config.data_format in {'pickle', 'json'}:
        if get_conf.config.data_format == 'pickle':
            mode += 'b'
        with open(filename, mode) as f:
            f.write(dump_data(data))
    elif get_conf.config.data_format == 'db':
        save_articles(data)

def load_from_somewhere(filename=None):
    mode = 'r'
    if get_conf.config.data_format == 'db':
        return select_all_articles()
    else:
        if get_conf.config.data_format == 'pickle':
            mode += 'b'
        with open(filename, mode) as f:
            return load_data(f.read())
