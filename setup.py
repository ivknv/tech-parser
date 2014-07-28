#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name="TechParser",
	version="1.2",
	author="Ivan Konovalov",
	author_email="rvan.mega@gmail.com",
	description="Lets You parse articles from various related to IT sites.",
	url="https://github.com/SPython/tech-parser",
	download_url="https://github.com/SPython/tech-parser/tarball/1.2",
	keywords=["parser", "article", "web"],
	classifiers=[],
	packages=["TechParser"],
	package_data={"TechParser": ["templates/*",
		"static/style.css", "static/icons/*"]})
