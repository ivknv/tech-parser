#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from grab.error import GrabError
import re
from lxml.etree import tostring

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
	s = s.replace('"', '&quot')
	s = s.replace(u'»', '&raquo;')
	s = s.replace(u'«', '&laquo;')
	
	return s

def parse_article_image(article, site_url=''):
	try:
		img = article.cssselect('img:first-child')[0]
		img.set('class', '')
		img.set('id', '')
		img.set('align', '')
		img.set('src', absolutize_link(img.get('src'), site_url))
		return tostring(img).strip()
	except IndexError:
		return b''
	except AttributeError:
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
	if len(s) > 300:
		return s[:300] + '...'
	elif not len(s):
		return 'No summary text available.'
	return s

def get_articles(grab_object, title_path, link_path, source, site_url="",
		summary_path=''):
	posts = []
		
	post_links = grab_object.css_list(link_path)
	post_titles = grab_object.css_list(title_path)
	if summary_path:
		summary = grab_object.css_list(summary_path)
		for i in summary:
			for j in i.getchildren():
				if j.tag in ['script', 'style']:
					i.remove(j)
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
			summary_text = summary_text.text_content().strip()
			summary_text = article_image + cut_text(summary_text)
		except AttributeError:
			summary_text = cut_text(remove_tags(summary_text).strip())
		
		posts.append(
			{"title": escape_title(title),
			"link": unicode_(link),
			"source": source,
			"summary": summary_text})
	
	return posts
