#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import db
import sqlite3

try:
    import psycopg2
except ImportError:
    pass

def SERIAL(database):
    if database.db not in {'sqlite', 'postgresql'}:
        raise UnsupportedDBError()
    if database.db == 'sqlite':
        return 'INTGER PRIMARY KEY AUTOINCREMENT'
    return 'SERIAL'

def DATETIME(database):
    if database.db not in {'sqlite', 'postgresql'}:
        raise UnsupportedDBError()
    if database.db == 'sqlite':
        return 'DATETIME'
    return 'TIMESTAMP'

def __expiration_date(database):
    if database.db not in {'sqlite', 'postgresql'}:
        raise UnsupportedDBError()
    if database.db == 'sqlite':
        return '(datetime(\'now\', \'+1 years\'))'
    return 'now() + INTERVAL \'1 year\''

def alter_main_database(verbose=False):
    main_db = db.Database.main_database
    if main_db.db == 'sqlite':
        DBError = sqlite3.OperationalError
    elif main_db.db == 'postgresql':
        DBError = psycopg2.ProgrammingError
    TABLES = ({'name': 'interesting_articles',
        'columns': ({'name': 'id', 'type': SERIAL(main_db)},
            {'name': 'title', 'type': 'TEXT'},
            {'name': 'link', 'type': 'TEXT UNIQUE'},
            {'name': 'summary', 'type': 'TEXT'},
            {'name': 'source', 'type': 'TEXT'},
            {'name': 'fromrss', 'type': 'INTEGER'},
            {'name': 'icon', 'type': 'TEXT'},
            {'name': 'color', 'type': 'TEXT'})},
        {'name': 'blacklist',
        'columns': ({'name': 'id', 'type': SERIAL(main_db)},
            {'name': 'title', 'type': 'TEXT'},
            {'name': 'link', 'type': 'TEXT UNIQUE'},
            {'name': 'summary', 'type': 'TEXT'},
            {'name': 'source', 'type': 'TEXT'},
            {'name': 'fromrss', 'type': 'INTEGER'},
            {'name': 'icon', 'type': 'TEXT'},
            {'name': 'color', 'type': 'TEXT'})},
        {'name': 'sessions',
        'columns': ({'name': 'id', 'type': SERIAL(main_db)},
            {'name': 'sid', 'type': 'TEXT UNIQUE'},
            {'name': 'expires', 'type': DATETIME(main_db),
                'default': __expiration_date(main_db)})},
        {'name': 'variables',
        'columns': ({'name': 'id', 'type': SERIAL(main_db)},
            {'name': 'name', 'type': 'TEXT UNIQUE'},
            {'name': 'value', 'type': 'TEXT'})},
        {'name': 'blacklist',
         'columns': ({'name': 'id', 'type': SERIAL(main_db)},
                     {'name': 'title', 'type': 'TEXT'},
                     {'name': 'link', 'type': 'TEXT UNIQUE'},
                     {'name': 'summary', 'type': 'TEXT'},
                     {'name': 'source', 'type': 'TEXT'},
                     {'name': 'fromrss', 'type': 'INTEGER'},
                     {'name': 'icon', 'type': 'TEXT'},
                     {'name': 'color', 'type': 'TEXT'},
                     {'name': 'page_number', 'type': 'INTEGER'})})
    
    for table in TABLES:
        base_q = 'ALTER TABLE {0} ADD COLUMN {{0}} {{1}};'
        base_q = base_q.format(table['name'])
        for column in table['columns']:
            column_name = column['name']
            default_value = column.get('default', None)
            if default_value is not None:
                column_type = column['type'] + ' DEFAULT ' + default_value
            else:
                column_type = column['type']
            q = base_q.format(column_name, column_type)
            try:
                main_db.execute_query(db.Query(main_db.db, q))
                if verbose:
                    print(q)
            except DBError as error:
                main_db.con.rollback()
                error_msg = str(error)
                if verbose and ('exists' in error_msg or 'duplicate' in error_msg):
                    msg = "'{0}' column of table '{1}' already exists"
                    print(msg.format(column_name, table['name']))

def alter_archive_database(verbose=False):
    archive_db = db.Database.databases['Archive']
    if archive_db.db == 'sqlite':
        DBError = sqlite3.OperationalError
    elif archive_db.db == 'postgresql':
        DBError = psycopg2.ProgrammingError
    TABLES = ({'name': 'articles',
        'columns': ({'name': 'id', 'type': SERIAL(archive_db)},
            {'name': 'title', 'type': 'TEXT'},
            {'name': 'link', 'type': 'TEXT UNIQUE'},
            {'name': 'source', 'type': 'TEXT'})},)
    
    for table in TABLES:
        base_q = 'ALTER TABLE {0} ADD COLUMN {{0}} {{1}};'
        base_q = base_q.format(table['name'])
        for column in table['columns']:
            column_name = column['name']
            default_value = column.get('default', None)
            if default_value is not None:
                column_type = column['type'] + ' DEFAULT ' + default_value
            else:
                column_type = column['type']
            q = base_q.format(column_name, column_type)
            try:
                archive_db.execute_query(db.Query(archive_db.db, q))
                if verbose:
                    print(q)
            except DBError as error:
                archive_db.con.rollback()
                error_msg = str(error)
                if verbose and ('exists' in error_msg or 'duplicate' in error_msg):
                    msg = "'{0}' column of table '{1}' already exists"
                    print(msg.format(column_name, table['name']))
