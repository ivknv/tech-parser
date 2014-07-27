#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import habrahabr
from TechParser import venturebeat
from TechParser import engadget
from TechParser import techcrunch
from TechParser import techrepublic
from TechParser import readwrite
from TechParser import smashingmagazine
from TechParser import gizmodo
from TechParser import slashdot
from TechParser import androidcentral
from TechParser import verge

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
		
		# Doesn't work anymore
		#"Read/Write Web": {
		#	"link": "readwrite.com",
		#	"module": readwrite,
		#	"kwargs": {}
		#},
		
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

filters = {
	"All": {
		"has": [],
		"or": [],
		"not": []
	}
}

update_interval = 1800 # Parse articles every 30 minutes

host = "0.0.0.0" # Server host
port = "8080" # Server port

# Server to use
server = "auto" # See http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend
