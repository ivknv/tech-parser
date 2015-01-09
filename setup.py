#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

v = "1.8.2"

setup(name="TechParser",
	version=v,
	author="Ivan Konovalov",
	author_email="rvan.mega@gmail.com",
	description="Lets You parse articles from various related to IT sites.",
	url="https://github.com/SPython/tech-parser",
	download_url="https://github.com/SPython/tech-parser/tarball/"+v,
	keywords=["parser", "article", "web", "ranking", "rss"],
	requires=["grab", "mako", "bottle", "Daemo"],
	classifiers=[],
	packages=["TechParser", "TechParser.parsers"],
	package_data={"TechParser": ["templates/*", "static/tech-parser.js",
		"static/jquery.touchSwipe.min.js", "static/fonts/*",
		"static/style.css", "static/jquery-2.1.1.min.js", "static/icons/*"]})
