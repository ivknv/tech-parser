#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

from TechParser.py2x import urlparse
from TechParser import get_conf

try:
	import psycopg2
except ImportError:
	pass

if get_conf.config is None:
	get_conf.set_config_auto()

get_conf.auto_fix_config()

class Database(object):
	"""Used to automatically determine which query to execute"""
	main_database = None
	
	def __init__(self, db='sqlite'):
		self.con = connect_db(db)
		self.cur = self.con.cursor()
		self.db = db
		if db == 'sqlite':
			self.execute = lambda *args, **kwargs: self.cur.executescript(*args, **kwargs)
		else:
			self.execute = lambda *args, **kwargs: self.cur.execute(*args, **kwargs)
		self.setup()
	
	def commit(self):
		self.con.commit()
	
	def setup(self):
		"""Setup database"""
		
		self.execute_query(Q_SETUP)
	
	def close(self):
		self.commit()
		self.con.close()
	
	def execute_query(self, query, parameters=None):
		if parameters is None:
			parameters = query.parameters
		if isinstance(query, MultiDBQuery):
			if self.db == 'sqlite':
				self.cur.executescript(query.sqlite_query.query, parameters)
			else:
				self.execute(query.postgresql_query.query, parameters)
		else:
			self.execute(query.query, parameters)
		self.commit()
	
	def fetchone(self):
		return self.cur.fetchone()
	
	def fetchall(self):
		return self.cur.fetchall()
	
	def __del__(self):
		self.close()
	
	@staticmethod
	def initialize():
		Database.main_database = Database(get_conf.config.db)

class Query(object):
	"""Simple single datbase query. Should be used when query \
can be executed on all databases. Otherwise MultiDBQuery should be used"""
	
	def __init__(self, db='sqlite', query=''):
		self.db = db
		self.query = query
		self.parameters = tuple()
	
class MultiDBQuery(object):
	"""Query for multiple databases."""
	
	def __init__(self, *queries):
		for query in queries:
			if query.db == 'sqlite':
				self.sqlite_query = query
			elif query.db == 'postgresql':
				self.postgresql_query = query
		self.parameters = tuple()

def which_db(db):
	"""Determine which database should be used and \
return corresponding functions to connect it"""
	
	if db == 'postgresql':
		try:
			connect = lambda: psycopg2.connect(**parse_dburl())
		except NameError:
			arg = os.path.join(get_conf.logdir, 'interesting.db')
			connect = lambda: sqlite3.connect(arg)
	elif db == 'sqlite':
		arg = os.path.join(get_conf.logdir, 'interesting.db')
		connect = lambda: sqlite3.connect(arg)
	else:
		raise Exception('db must be sqlite or postgresql')
	
	return connect

def parse_dburl(var='DATABASE_URL'):
	"""Parse database URL from environment variable"""
	
	parsed = urlparse(os.environ.get(var, ''))
	
	return {'user': parsed.username,
			'password': parsed.password,
			'host': parsed.hostname,
			'port': parsed.port,
			'dbname': parsed.path[1:]}

def connect_db(db='sqlite'):
	return which_db(db)()

# Those queries are special because they are used in Database.setup
Q_SETUP_SQLITE = Query('sqlite',
	'''CREATE TABLE IF NOT EXISTS interesting_articles
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT, link TEXT, summary TEXT, source TEXT,
			fromrss INTEGER, icon TEXT, color TEXT,
			UNIQUE(link));
	CREATE TABLE IF NOT EXISTS blacklist
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
			fromrss INTEGER, icon TEXT, color TEXT,
			title TEXT, link TEXT, summary TEXT, source TEXT,
			UNIQUE(link))''')

Q_SETUP_POSTGRESQL = Query('postgresql',
	'''CREATE TABLE IF NOT EXISTS interesting_articles
		(id SERIAL,	title TEXT, link TEXT, summary TEXT,
			fromrss INTEGER, icon TEXT, color TEXT,
			source TEXT, UNIQUE(link));
	CREATE TABLE IF NOT EXISTS blacklist
		(id SERIAL, title TEXT, link TEXT, summary TEXT,
			fromrss INTEGER, icon TEXT, color TEXT,
			source TEXT, UNIQUE(link))''')

Q_SETUP = MultiDBQuery(Q_SETUP_SQLITE, Q_SETUP_POSTGRESQL)
