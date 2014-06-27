#!/usr/bin/env python
# -*- coding: utf-8 -*-

import habrahabr
import venturebeat
import engadget
import techcrunch
import techrepublic
import readwrite
import smashingmagazine
import gizmodo
import slashdot

sites_to_parse = {
		"Habrahabr": {
			"link": "habrahabr.ru",
			"module": habrahabr,
			"kwargs": {}
		},
		
		"VentureBeat": {
			"link": "venturebeat.com",
			"module": venturebeat,
			"kwargs": {"start_page": 1, "end_page": 3}
		},
		
		"Engadget": {
			"link": "engadget.com",
			"module": engadget,
			"kwargs": {"start_page": 1, "end_page": 5}
		},
		
		"Slashdot": {
			"link": "slashdot.org",
			"module": slashdot,
			"kwargs": {"start_page": 1, "end_page": 3}
		},
		
		"Gizmodo": {
			"link": "gizmodo.com",
			"module": gizmodo,
			"kwargs": {}
		},
		
		"TechCrunch": {
			"link": "techcrunch.com",
			"module": techcrunch,
			"kwargs": {}
		},
		
		"Read/Write Web": {
			"link": "readwrite.com",
			"module": readwrite,
			"kwargs": {}
		},
		
		"Tech Republic": {
			"link": "techrepublic.com",
			"module": techrepublic,
			"kwargs": {}
		},
		
		"Smashing Magazine": {
			"link": "www.smashingmagazine.com",
			"module": smashingmagazine,
			"kwargs": {}
		}
	}

update_every = 1800 # Update every 30 minutes
