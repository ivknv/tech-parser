#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grab
from TechParser import parser

def get_articles(start_page=1, end_page=5):
	g = grab.Grab()
	
	parser.setup_grab(g)
	
	posts = []
	css_path = "article"# header h2 span a"
	title_path = "header h2 span a"
	summary_path = ".body .p"
	
	for i in range(start_page-1, end_page):
		g.go("http://slashdot.org?page=%i" %i)
		
		for article in g.css_list(css_path):
			article.make_links_absolute(g.response.url)
			try:
				link = article.cssselect(title_path)[0]
			except IndexError:
				continue
			title = parser.escape_title(link.text_content())
			link = link.get("href")
			try:
				summary = article.cssselect(summary_path)[0]
				for i in summary:
					for j in i.getchildren():
						if j.tag in ['script', 'style']:
							i.remove(j)
				summary = parser.cut_text(summary.text_content().strip())
			except IndexError:
				summary = 'No summary text available.'
			posts.append({'title': title,
						'summary': summary,
						'link': link,
						'source': 'slashdot'})

		
#		posts += parser.get_articles(g, css_path, css_path,
#			"slashdot", summary_path=summary_path)
		
	return posts
