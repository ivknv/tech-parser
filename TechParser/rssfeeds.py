#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from TechParser.recommend import setup_db
from PIL import Image
import os
import re

try:
	from urllib.request import urlopen
except ImportError:
	from urllib import urlopen

module_path = os.path.dirname(os.path.realpath(__file__))
static_dir_path = os.path.join(module_path, 'static')
icon_dir = os.path.join(static_dir_path, 'icons')

def add_feed(url, name, db='sqlite'):
	res = feedparser.parse(url)
	if 'image' in res.feed:
		image_src = res.feed['image']['href']
		urlo = urlopen(image_src)
		urlor = urlo.read()
		f = open(os.path.join(icon_dir, name + '.ico'), 'wb')
		f.write(urlor)
		f.close()
		im = Image.open(os.path.join(icon_dir, name + '.ico'))
		pixels = list(im.getdata())
		print(pixels)
		average = [0, 0, 0]
		for pixel in pixels:
			average[0] += pixel[0]
			average[1] += pixel[1]
			average[2] += pixel[2]
		n = len(pixels)
		average[0] /= n
		average[1] /= n
		average[2] /= n
	
		f = open(os.path.join(static_dir_path), 'style.css', 'a')
		f.write('''
.%s {
	color: rgb(%s);
}''' %(name, ','.join(map(lambda x: str(x), average))))
		f.close()
	
	add_feed_to_db(url, name, db)

def add_feed_to_db(url, name, db='sqlite'):
	setup_db(db)
	
	connect, args, kwargs = which_db(db)
	
	con = connect(*args, **kwargs)
	cur = con.cursor()
	sqlite_code = """INSERT INTO rss_feeds(name, url) VALUES(?, ?);"""
	postgres_code = """INSERT INTO rss_feeds(name, url) VALUES(%s, %s);"""
	
	if db == 'sqlite':
		code = sqlite_code
	else:
		code = postgres_code
	
	cur.execute(code, (name, url))
	con.commit()
	
	con.close()
