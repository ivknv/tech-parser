#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

from TechParser.py2x import urlparse, zip_longest
from TechParser import get_conf

try:
	import psycopg2
except ImportError:
	pass

if get_conf.config is None:
	get_conf.set_config_auto()

get_conf.auto_fix_config()

class DBError(Exception):
	pass

class UnsupportedDBError(DBError):
	def __init__(self, db):
		msg = '\'{0}\' database is not supported (yet)'.format(db)
		super(UnsupportedDBException, self).__init__(msg)

class Database(object):
	"""Used to automatically determine which query to execute"""
	main_database = None
	databases = {}
	_last_id = 0
	
	def __init__(self, db='sqlite', name='', con=None, setup_query=None):
		if con is None:
			self.con = connect_db(db)
		else:
			self.con = con
		self.cur = self.con.cursor()
		self.db = db
		self.setup_query = setup_query
		if db == 'sqlite':
			def func(q, p):
				for (i, j) in zip_longest(q.split(';'), p, fillvalue=tuple()):
					if len(i):
						self.cur.execute(i, j)
			self.execute = func
		elif db == 'postgresql':
			self.execute = lambda q, p: self.cur.execute(q, p[0] if p else [])
		self.id = Database._last_id
		self.userData = None
		Database._last_id += 1
		if not name:
			self.name = 'Database-{0}'.format(self.id)
		else:
			self.name = name
		self.setup()
	
	@staticmethod
	def register(database):
		Database.databases[database.name] = database
	
	def commit(self):
		self.con.commit()
	
	def setup(self):
		"""Setup database"""
		
		if self.setup_query is not None:
			self.execute_query(self.setup_query)
	
	def close(self):
		self.commit()
		self.con.close()
		try:
			Database.databases.pop(self.name)
		except KeyError:
			pass
	
	def execute_query(self, query, parameters=None):
		if parameters is None:
			parameters = query.parameters
		if isinstance(query, MultiDBQuery):
			if self.db == 'sqlite':
				self.execute(query.sqlite_query.query, parameters)
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
	
	def __exit__(self):
		self.close()
	
	def __repr__(self):
		return '<Database name=\'{0}\', id={1}, db=\'{2}\'>'.format(self.name, self.id, self.db)
	
def initialize_main_database():
	"""Setup main database"""
	
	Database.main_database = Database(get_conf.config.db, 'Main-Database',
		setup_query=Q_SETUP)
	if get_conf.config.db == 'sqlite':
		Database.main_database.userData = sqlite3.IntegrityError
	else:
		Database.main_database.userData = psycopg2.IntegrityError
	Database.register(Database.main_database)

def initialize_archive_db():
	"""Setup archive database"""
	logdir = os.path.join(os.path.expanduser('~'), '.tech-parser')
	con = sqlite3.connect(os.path.join(logdir, "archive.db"))
	archiveDB = Database(db='sqlite', name='Archive', con=con, setup_query=Q_SETUP_ARCHIVE)
	archiveDB.userData = sqlite3.IntegrityError
	Database.register(archiveDB)

class Query(object):
	"""Simple single database query. Should be used when query \
can be executed by all databases. Otherwise MultiDBQuery should be used"""
	
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
		raise UnsupportedDBError(db)
	
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
Q_SETUP_ARCHIVE_SQLITE = Query('sqlite',
	'''CREATE TABLE IF NOT EXISTS articles
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT, link TEXT, source TEXT, UNIQUE(link));''')
Q_SETUP_ARCHIVE_POSTGRESQL = Query('postgresql',
	'''CREATE TABLE IF NOT EXISTS articles
		(id SERIAL, title TEXT, link TEXT, source TEXT, UNIQUE(link));''')

Q_SETUP = MultiDBQuery(Q_SETUP_SQLITE, Q_SETUP_POSTGRESQL)
Q_SETUP_ARCHIVE = MultiDBQuery(Q_SETUP_ARCHIVE_SQLITE, Q_SETUP_ARCHIVE_POSTGRESQL)
