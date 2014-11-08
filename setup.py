#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

v = "1.7.11"

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
	packages=["TechParser"],
	package_data={"TechParser": ["templates/*",
		"static/jquery.touchSwipe.min.js", "static/fonts/*",
		"static/style.css", "static/jquery-2.1.1.min.js", "static/icons/*"]})
