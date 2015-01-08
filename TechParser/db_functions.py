#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser.query import *
from TechParser import db, get_conf
import sqlite3
import uuid
from Crypto import Random
import datetime

try:
	import psycopg2
except ImportError:
	pass

def format_date(date):
	try:
		return datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S.%f')
	except ValueError:
		return datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')

def date_fromstr(s):
	try:
		return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
	except ValueError:
		return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')

def todatetime(date_or_string):
	if isinstance(date_or_string, str):
		return date_fromstr(s)
	
	return date_or_string

def remove_from_blacklist(link):
	"""Remove article from blacklist by link"""
	
	db.Database.main_database.execute_query(Q_DELETE_FROM_BLACKLIST, [(link,)])

def remove_from_history(link):
	"""Remove article from history by link"""
	
	db.Database.main_database.execute_query(Q_DELETE_FROM_HISTORY, [(link,)])

def add_to_blacklist(article):
	"""Add article to blacklist"""
	
	IntegrityError = db.Database.main_database.userData # userData contains exception
	
	try:
		title = article['title']
		link = article['link']
		summary = article['summary']
		source = article['source']
		fromrss = article.get('fromrss', 0)
		icon = article.get('icon', '')
		color = article.get('color', '#000')
		parameters = [(title, link, summary, fromrss, icon, color, source)]
		db.Database.main_database.execute_query(Q_ADD_TO_BLACKLIST, parameters)
	except IntegrityError:
		pass

def add_to_interesting(article):	
	"""Add article to history"""
	
	IntegrityError = db.Database.main_database.userData # userData contains exception
	
	try:
		title = article['title']
		link = article['link']
		summary = article['summary']
		source = article['source']
		fromrss = article.get('fromrss', 0)
		icon = article.get('icon', '')
		color = article.get('color', '#000')
		parameters = [(title, link, summary, fromrss, icon, color, source)]
		
		db.Database.main_database.execute_query(Q_ADD_TO_HISTORY, parameters)
	except IntegrityError:
		pass

def get_blacklist():
	"""Get list of articles from blacklist"""
	
	db.Database.main_database.execute_query(Q_GET_BLACKLIST)
	
	return [{'title': x[0],
			'link': x[1],
			'summary': x[2],
			'fromrss': x[3],
			'icon': x[4],
			'color': x[5],
			'source': x[6]} for x in db.Database.main_database.fetchall()]

def get_interesting_articles():
	"""Get list of articles from history (that were marked as interesting)"""
	
	db.Database.main_database.execute_query(Q_GET_HISTORY)
	
	return [{'title': x[0],
			'link': x[1],
			'summary': x[2],
			'fromrss': x[3],
			'icon': x[4],
			'color': x[5],
			'source': x[6]} for x in db.Database.main_database.fetchall()]

def generate_sessionid(num_bytes=16):
	return uuid.UUID(bytes=Random.get_random_bytes(num_bytes))

def add_session():
	sid = str(generate_sessionid())
	db.Database.main_database.execute_query(Q_ADD_SESSIONID, [(sid,)])
	return sid

def delete_session(sid):
	db.Database.main_database.execute_query(Q_DELETE_SESSIONID, [(sid,)])

def check_password(password):
	return get_conf.config.password == password

def check_session_existance(sid):
	remove_old_sessions()
	db.Database.main_database.execute_query(Q_CHECK_SESSIONID, [(sid,)])
	return not not db.Database.main_database.fetchone() # Convert result to boolean

def remove_old_sessions():
	db.Database.main_database.execute_query(Q_REMOVE_OLD_SESSIONIDS)
