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
        super(UnsupportedDBError, self).__init__(msg)

class Database(object):
    """Used to automatically determine which query to execute"""
    main_database = None
    databases = {}
    _last_id = 0
    
    def __init__(self, connect_func, db='sqlite', name='', setup_query=None):
        self.connect_func = connect_func
        self.open()
        self.db = db
        self.setup_query = setup_query
        if db == 'sqlite':
            def func(q, p):
                for (i, j) in zip_longest(q.split(';'), p, fillvalue=tuple()):
                    if len(i):
                        self.cur.execute(i, j)
            self.execute = func
        elif db == 'postgresql':
            def func(q, p):
                self.cur.execute(q, [j for i in p for j in i])
                
            self.execute = func
        self.id = Database._last_id
        self.userData = None
        Database._last_id += 1
        if not name:
            self.name = 'Database-{0}'.format(self.id)
        else:
            self.name = name
        self.setup()
    
    def open(self):
        self.con = self.connect_func()
        self.cur = self.con.cursor()
    
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

class MainDatabase(Database):
    def __init__(self):
        connect_func = which_db(get_conf.config.db)
        super(MainDatabase, self).__init__(connect_func,
            get_conf.config.db, 'Main-Database', setup_query=Q_SETUP)
        if get_conf.config.db == 'sqlite':
            self.userData = sqlite3.IntegrityError
        else:
            self.userData = psycopg2.IntegrityError
    
def initialize_main_database():
    """Setup main database"""
    
    Database.main_database = MainDatabase()
    Database.register(Database.main_database)

def initialize_archive_db():
    """Setup archive database"""
    
    if get_conf.config.archive_db_path == 'default':
        path = os.path.join(get_conf.logdir, 'archive.db')
        get_conf.config.archive_db_path = 'sqlite://{0}'.format(path)
    
    parsed = parse_dburl(get_conf.config.archive_db_path)
    db = parsed['scheme']
    if db == 'sqlite':
        connect_func = lambda: sqlite3.connect(parsed['dbname'])
    elif db == 'postgres':
        db = 'postgresql'
        parsed.pop('scheme')
        connect_func = lambda: psycopg2.connect(**parsed)
    else:
        raise UnsupportedDBError(db)
    archiveDB = Database(connect_func, db, name='Archive',
        setup_query=Q_SETUP_ARCHIVE)
    if db == 'postgresql':
        archiveDB.userData = psycopg2.IntegrityError
    else:
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
return corresponding function to connect it"""
    
    if db == 'postgresql':
        parsed = parse_dburl(get_conf.config.db_path)
        parsed.pop('scheme')
        connect = lambda: psycopg2.connect(**parsed)
    elif db == 'sqlite':
        arg = os.path.join(get_conf.logdir, 'interesting.db')
        connect = lambda: sqlite3.connect(arg)
    else:
        raise UnsupportedDBError(db)
    
    return connect

def parse_dburl(s):
    """Parse URL to database from string"""
    
    parsed = urlparse(s)
    
    res = {'scheme': parsed.scheme,
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'dbname': parsed.path}
    if parsed.scheme != 'sqlite':
        res['dbname'] = parsed.path[1:]
    return res

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
            UNIQUE(link));
    CREATE TABLE IF NOT EXISTS sessions
        (id INTEGER PRIMARY KEY AUTOINCREMENT, sid TEXT,
            expires DATETIME DEFAULT (datetime('now', '+1 years')),
            UNIQUE(sid));
    CREATE TABLE IF NOT EXISTS variables
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, value TEXT);
    CREATE TABLE IF NOT EXISTS articles
        (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, link TEXT, summary TEXT, source TEXT,
            fromrss INTEGER, icon TEXT, color TEXT, page_number INTEGER, UNIQUE(link))''')

Q_SETUP_POSTGRESQL = Query('postgresql',
    '''CREATE TABLE IF NOT EXISTS interesting_articles
        (id SERIAL,    title TEXT, link TEXT, summary TEXT,
            fromrss INTEGER, icon TEXT, color TEXT,
            source TEXT, UNIQUE(link));
    CREATE TABLE IF NOT EXISTS blacklist
        (id SERIAL, title TEXT, link TEXT, summary TEXT,
            fromrss INTEGER, icon TEXT, color TEXT,
            source TEXT, UNIQUE(link));
    CREATE TABLE IF NOT EXISTS sessions
        (id SERIAL, sid TEXT,
            expires TIMESTAMP DEFAULT now() + INTERVAL '1 year', UNIQUE(sid));
    CREATE TABLE IF NOT EXISTS variables
        (id SERIAL, name TEXT UNIQUE, value TEXT);
    CREATE TABLE IF NOT EXISTS articles
        (id SERIAL, title TEXT, link TEXT, summary TEXT, source TEXT,
            fromrss INTEGER, icon TEXT, color TEXT, page_number INTEGER, UNIQUE(link))''')
Q_SETUP_ARCHIVE_SQLITE = Query('sqlite',
    '''CREATE TABLE IF NOT EXISTS articles
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, link TEXT, source TEXT, UNIQUE(link));''')
Q_SETUP_ARCHIVE_POSTGRESQL = Query('postgresql',
    '''CREATE TABLE IF NOT EXISTS articles
        (id SERIAL, title TEXT, link TEXT, source TEXT, UNIQUE(link));''')

Q_SETUP = MultiDBQuery(Q_SETUP_SQLITE, Q_SETUP_POSTGRESQL)
Q_SETUP_ARCHIVE = MultiDBQuery(Q_SETUP_ARCHIVE_SQLITE, Q_SETUP_ARCHIVE_POSTGRESQL)
