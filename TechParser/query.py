#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser.db import Query, MultiDBQuery
from TechParser.db import Q_SETUP_SQLITE, Q_SETUP_POSTGRESQL, Q_SETUP

Q_DELETE_FROM_BLACKLIST_SQLITE = Query('sqlite',
	'DELETE FROM blacklist WHERE link=?;')
Q_DELETE_FROM_BLACKLIST_POSTGRESQL = Query('postgresql',
	'DELETE FROM blacklist WHERE link=%s;')
Q_DELETE_FROM_HISTORY_SQLITE = Query('sqlite',
	'DELETE FROM interesting_articles WHERE link=?;')
Q_DELETE_FROM_HISTORY_POSTGRESQL = Query('postgresql'
	'DELETE FROM interesting_articles WHERE link=%s;')
Q_ADD_TO_BLACKLIST_SQLITE = Query('sqlite',
	'''INSERT INTO blacklist(title, link, summary, fromrss, icon, color, source)
		VALUES(?, ?, ?, ?, ?, ?, ?);''')
Q_ADD_TO_BLACKLIST_POSTGRESQL = Query('postgresql',
	'''INSERT INTO blacklist(title, link, summary, fromrss, icon, color, source)
		VALUES(%s, %s, %s, %s, %s, %s, %s);''')
Q_ADD_TO_HISTORY_SQLITE = Query('sqlite',
	'''INSERT INTO interesting_articles(title, link, summary, fromrss, icon, color, source)
		VALUES(?, ?, ?, ?, ?, ?, ?);''')
Q_ADD_TO_HISTORY_POSTGRESQL = Query('postgresql',
	'''INSERT INTO interesting_articles(title, link, summary, fromrss, icon, color, source)
		VALUES(%s, %s, %s, %s, %s, %s, %s);''')
Q_SAVE_ARTICLES_SQLITE = Query('sqlite',
	'INSERT INTO articles(title, link, source) VALUES(?, ?, ?);')
Q_SAVE_ARTICLES_POSTGRESQL = Query('postgresql',
	'INSERT INTO articles(title, link, source) VALUES(%s, %s, %s);')
Q_ADD_SESSIONID_SQLITE = Query('sqlite',
	'INSERT INTO sessions(sid) VALUES(?);')
Q_ADD_SESSIONID_POSTGRESQL = Query('postgresql',
	'INSERT INTO sessions(sid) VALUES(%s);')
Q_DELETE_SESSIONID_SQLITE = Query('sqlite',
	'DELETE FROM sessions WHERE sid=?;')
Q_DELETE_SESSIONID_POSTGRESQL = Query('sqlite',
	'DELETE FROM sessions WHERE sid=%s;')
Q_CHECK_SESSIONID_SQLITE = Query('sqlite',
	'SELECT id FROM sessions WHERE sid=?;')
Q_CHECK_SESSIONID_POSTGRESQL = Query('postgresql',
	'SELECT id FROM sessions WHERE sid=%s;')
Q_REMOVE_OLD_SESSIONIDS_SQLITE = Query('sqlite',
	'DELETE FROM sessions WHERE expires <= date(\'now\');')
Q_REMOVE_OLD_SESSIONIDS_POSTGRESQL = Query('postgresql',
	'DELETE FROM sessions WHERE expires <= now();')

Q_DELETE_FROM_BLACKLIST = MultiDBQuery(Q_DELETE_FROM_BLACKLIST_SQLITE,
	Q_DELETE_FROM_BLACKLIST_POSTGRESQL)
Q_DELETE_FROM_HISTORY = MultiDBQuery(Q_DELETE_FROM_HISTORY_SQLITE,
	Q_DELETE_FROM_HISTORY_POSTGRESQL)
Q_ADD_TO_BLACKLIST = MultiDBQuery(Q_ADD_TO_BLACKLIST_SQLITE,
	Q_ADD_TO_BLACKLIST_POSTGRESQL)
Q_ADD_TO_HISTORY = MultiDBQuery(Q_ADD_TO_HISTORY_SQLITE,
	Q_ADD_TO_HISTORY_POSTGRESQL)
Q_GET_BLACKLIST = Query('all', '''SELECT title, link, summary, fromrss, icon, color, source
	FROM blacklist ORDER BY id DESC;''')
Q_GET_HISTORY = Query('all', '''SELECT title, link, summary, fromrss, icon, color, source
	FROM interesting_articles ORDER BY id DESC;''')
Q_SAVE_ARTICLES = MultiDBQuery(Q_SAVE_ARTICLES_SQLITE, Q_SAVE_ARTICLES_POSTGRESQL)
Q_ADD_SESSIONID = MultiDBQuery(Q_ADD_SESSIONID_SQLITE, Q_ADD_SESSIONID_POSTGRESQL)
Q_DELETE_SESSIONID = MultiDBQuery(Q_DELETE_SESSIONID_SQLITE, Q_DELETE_SESSIONID_POSTGRESQL)
Q_CHECK_SESSIONID = MultiDBQuery(Q_CHECK_SESSIONID_SQLITE, Q_CHECK_SESSIONID_POSTGRESQL)
Q_REMOVE_OLD_SESSIONIDS = MultiDBQuery(Q_REMOVE_OLD_SESSIONIDS_SQLITE, Q_REMOVE_OLD_SESSIONIDS_POSTGRESQL)
