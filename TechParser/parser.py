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

def absolutize_link(link, site_url):
	if link.startswith("//"):
		link = "http:" + link
	elif link.startswith("/"):
		link = "http://" + site_url + link
	
	return link

def get_articles(grab_object, title_path, link_path, source, site_url=""):
	posts = []
		
	post_links = grab_object.css_list(link_path)
	post_titles = grab_object.css_list(title_path)
	
	for (title, link) in zip(post_links, post_titles):
		title = title.text_content()
		link = absolutize_link(link.get("href"), site_url)
		
		posts.append(
			{"title": unicode_(title).strip(),
			"link": link,
			"source": source})
	
	return posts
