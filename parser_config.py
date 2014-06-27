#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SiteParse import habrahabr
from SiteParse import venturebeat
from SiteParse import engadget
from SiteParse import techcrunch
from SiteParse import techrepublic
from SiteParse import readwrite
from SiteParse import smashingmagazine
from SiteParse import gizmodo
from SiteParse import slashdot
from SiteParse import androidcentral
from SiteParse import verge

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
		},
		
		"Android Central": {
			"link": "www.androidcentral.com",
			"module": androidcentral,
			"kwargs": {"start_page": 1, "end_page": 5}
		},
		
		"The Verge": {
			"link": "www.theverge.com",
			"module": verge,
			"kwargs": {}
		}
	}

update_interval = 1800 # Parse articles every 30 minutes

host = "0.0.0.0" # Server host
port = "8080" # Server port
