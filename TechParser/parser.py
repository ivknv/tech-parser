#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from grab.error import GrabError
import re
from lxml.html import fromstring, tostring
from lxml.etree import Error as LXMLError
import feedparser

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def setup_grab(grab_object):
	grab_object.setup(
		hammer_mode=True,
		hammer_timeouts=((10, 15), (20, 30), (25, 40)))

def absolutize_link(link, site_url):
	if link.startswith("//"):
		link = "http:" + link
	elif link.startswith("/"):
		link = "http://" + site_url + link
	
	return link

def remove_tags(s):
	return re.sub(r'<.*?>', '', s)

def escape_title(s):
	s = s.replace('&', '&amp;')
	s = s.replace('<', '&lt;')
	s = s.replace('>', '&gt;')
	s = s.replace('"', '&quot;')
	s = s.replace(u'»', '&raquo;')
	s = s.replace(u'«', '&laquo;')
	
	return s

def parse_article_image(article, site_url=''):
	try:
		img = article.cssselect('img:first-child')[0]
		img.set('class', '')
		img.set('id', '')
		img.set('align', '')
		img.set('src', absolutize_link(img.get('src', ''), site_url))
		return tostring(img).strip()
	except IndexError:
		return b''
	except AttributeError as e:
		try:
			img = grab.Grab(article).css_one('img:first-child')
		except GrabError:
			return b''
		img.set('class', '')
		img.set('id', '')
		img.set('align', '')
		img.set('src', absolutize_link(img.get('src'), site_url))
		return tostring(img).strip()

def cut_text(s):
	splitted = s.split(' ')
	if len(splitted) > 50:
		return ' '.join(splitted[:50]) + '...'
	return s

def get_articles(grab_object, title_path, link_path, source, site_url="",
		summary_path=''):
	posts = []
		
	post_links = grab_object.css_list(link_path)
	post_titles = grab_object.css_list(title_path)
	if summary_path:
		summary = grab_object.css_list(summary_path)
		for i in summary:
			for j in i.cssselect('script') + i.cssselect('style'):
				j.drop_tree()
	else:
		summary = []
	
	while len(summary) < len(post_links):
		summary.append('')
	
	zip_object = zip(post_links, post_titles, summary)
	
	for (title, link, summary_text) in zip_object:
		title = unicode_(title.text_content()).strip()
		link = grab_object.make_url_absolute(link.get("href"))
		if len(summary_text):
			try:
				article_image = parse_article_image(summary_text,
					site_url).decode()
			except AttributeError:
				article_image = parse_article_image(summary_text, site_url)
		else:
			article_image = ''
		
		try:
			summary_text = summary_text.text_content()
			summary_text = article_image + cut_text(summary_text)
		except AttributeError:
			summary_text = cut_text(remove_tags(summary_text))
		
		posts.append(
			{"title": escape_title(title),
			"link": unicode_(link),
			"source": source,
			"summary": summary_text})
	
	return posts

def parse_rss(url, source, icon='', color='#000'):
	entries = get_articles_from_rss(url, source)
	return [{'fromrss': 1,
			'icon': icon,
			'color': color,
			'title': i['title'],
			'link': i['link'],
			'source': source,
			'summary': i['summary']}
				for i in entries]

def get_articles_from_rss(url, source, parse_image=True):
	parsed_entries = feedparser.parse(url).entries
	entries = []
	for entry in parsed_entries:
		cleaned = clean_text(entry['summary'], parse_image)
		text = cleaned[0]
		image = cleaned[1]
		if parse_image and not len(image):
			for link in entry['links']:
				if link.get('type', '').startswith('image/'):
					image = '<img src="{}" />'.format(link['href'])
					text = image + text
					break
		
		entries.append({'title': escape_title(entry['title']),
			'link': entry['link'],
			'source': source,
			'summary': text})
	
	return entries

def remove_bad_tags(s):
	elmt = fromstring(s)
	for bad in elmt.cssselect('script, style, iframe'):
		bad.drop_tree()
	
	return tostring(elmt).decode()

def clean_text(s, parse_image=True):
	try:
		image = parse_article_image(s).decode() if parse_image else ''
		return (image + cut_text(remove_tags((remove_bad_tags(s)))), image)
	except LXMLError:
		return ('', '')
