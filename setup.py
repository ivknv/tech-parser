#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name="TechParser",
	version="1.1",
	author="Ivan Konovalov",
	author_email="rvan.mega@gmail.com",
	description="Lets You parse articles from 10 sites.",
	packages=["TechParser"],
	package_data={"TechParser": ["templates/*",
		"static/style.css", "static/icons/*"]})
