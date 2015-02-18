#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp, os, json

logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

config = None

class Config(object):
    def __init__(self, hide=False, **kwargs):
        self.sites_to_parse = kwargs.get('sites_to_parse')
        
        for k,v in self.sites_to_parse.items():
            v.setdefault('hash', hash(k))
        
        self.rss_feeds = kwargs.get('rss_feeds')
        
        for k,v in self.rss_feeds.items():
            v.setdefault('hash', hash(k))
        
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
        self.json_config = kwargs.get('json_config', False)
        
        auto_fix_config(self)
    
    @staticmethod
    def from_module(module, hide=False):
        d = {}
        d['sites_to_parse'] = {k: {'module': v['module'].__name__,
            'kwargs': v['kwargs'],
            'hash': hash(k),
            'enabled': v['enabled']}
            for k,v in module.sites_to_parse.items()}
        d['rss_feeds'] = module.rss_feeds
        
        for k,v in d['rss_feeds'].items():
            v.setdefault('hash', hash(k))
        
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
        d['json_config'] = module.json_config
        
        return Config(**d)

def get_default_config():
    return __import__('TechParser.parser_config').parser_config

def get_config(fname):
    return imp.load_source('parser_config', fname)

def set_config(parser_config):
    global config
    
    config = parser_config
    
    for k,v in config.sites_to_parse.items():
        v.setdefault('hash', hash(k))

    for k,v in config.rss_feeds.items():
        v.setdefault('hash', hash(k))

def set_config_from_fname(fname):
    set_config(get_config(fname))

def set_default_config():
    set_config(get_default_config())

def set_config_from_logdir(fname):
    set_config_from_fname(os.path.join(logdir, fname))

def set_user_config():
    set_config_from_logdir('user_parser_config.py')

def config_from_json(json_str):
    conf = Config(**json.loads(json_str))
    conf.sites_to_parse = {k: {'module': __import__(v['module'], fromlist=['']),
                               'kwargs': v['kwargs'], 'enabled': v['enabled']}
                           for k,v in conf.sites_to_parse.items()}
    
    return conf

def set_config_auto():
    try:
        set_user_config()
    except IOError:
        set_default_config()
    
    if hasattr(config, 'json_config') and config.json_config:
        try:
            with open(os.path.join(logdir, 'user_parser_config.json'), 'r') as f:
                set_config(config_from_json(f.read()))
        except IOError:
            pass

def setdefault(obj, attr, value=None):
    try:
        getattr(obj, attr)
    except AttributeError:
        setattr(obj, attr, value)

def auto_fix_config(conf=None):
    if conf is None:
        conf = config
    setdefault(conf, 'sites_to_parse', {})
    
    for v in conf.sites_to_parse.values():
        v.setdefault('enabled', True)
    
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
    setdefault(conf, 'archive_db_path_variable', '')
    setdefault(conf, 'archive_db_path',
               os.environ.get(conf.archive_db_path_variable, 'default'))
    setdefault(conf, 'db_path_variable', '')
    setdefault(conf, 'db_path', os.environ.get(conf.db_path_variable, ''))
    setdefault(conf, 'data_format', 'pickle')
    setdefault(conf, 'password_variable', '')
    setdefault(conf, 'password', os.environ.get(conf.password_variable, ''))
    setdefault(conf, 'enable_pocket', False)
    setdefault(conf, 'json_config', False)
