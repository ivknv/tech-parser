#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

def setup_grab(grab_object):
	grab_object.setup(
		hammer_mode=True,
		hammer_timeouts=((10, 15), (20, 30), (25, 40)))

def get_articles(grab_object, title_path, link_path, source):
	posts = []
		
	post_links = grab_object.css_list(link_path)
	post_titles = grab_object.css_list(title_path)
	
	for (title, link) in zip(post_links, post_titles):
		title = title.text_content()
		link = link.get("href")
		
		posts.append(
			{
				"title": unicode_(title),
				"link": link,
				"source": source})
	
	return posts