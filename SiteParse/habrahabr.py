#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from lxml import etree

try:
	unicode_ = unicode
except NameError:
	unicode_ = str

g = grab.Grab()

g.go("http://habrahabr.ru")

pages = g.css_list("#layout .inner .content_left .posts_list .page-nav #nav-pages li a")

posts = []

for page in pages:
	g.go("http://habrahabr.ru"+page.get("href"))
	post_links = g.css_list("#layout .inner .content_left .posts_list .posts .post .title .post_title")
	
	for post_link in post_links:
		g.go(post_link.get("href"))
	
		if "company" in post_link.get("href"):
			title = g.css("#layout .inner .content_left .company_post .post .title .post_title")
			date = g.css("#layout .inner .content_left .company_post .post .published")
			text = g.css("#layout .inner .content_left .company_post .post .content")
			tags = g.css_list("#layout .inner .content_left .company_post .post .tags li a")
			hubs = g.css("#layout .inner .content_left .company_post .post .hubs")
		else:
			title = g.css("#layout .inner .content_left .post_show .post .title .post_title")
			date = g.css("#layout .inner .content_left .post_show .post .published")
			text = g.css("#layout .inner .content_left .post_show .post .content")
			tags = g.css_list("#layout .inner .content_left .post_show .post .tags li a")
			hubs = g.css_list("#layout .inner .content_left .post_show .post .hubs a")
		
		posts.append(
			{
				"title": unicode_(title),
				"date": unicode_(date.text_content()),
				"text": etree.tostring(text, encoding="unicode"),
				"tags": [[tag.get('href'), unicode_(tag.text_content())] for tag in tags],
				"hubs": [[hub.get('href'), unicode_(hub.text_content())] for hub in hubs]
			}
		)
