#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from TechParser import habrahabr
except ImportError:
	import habrahabr

try:
	from TechParser import venturebeat
except ImportError:
	import venturebeat

try:
	from TechParser import engadget
except ImportError:
	import engadget

try:
	from TechParser import techcrunch
except ImportError:
	import techcrunch

try:
	from TechParser import techrepublic
except ImportError:
	import techrepublic

#try:
#	from TechParser import readwrite
#except ImportError:
#	import readwrite

try:
	from TechParser import smashingmagazine
except ImportError:
	import smashingmagazine

try:
	from TechParser import gizmodo
except ImportError:
	import gizmodo

try:
	from TechParser import slashdot
except ImportError:
	import slashdot

try:
	from TechParser import androidcentral
except ImportError:
	import androidcentral

try:
	from TechParser import verge
except ImportError:
	import verge

try:
	from TechParser import topdesignmag
except ImportError:
	import topdesignmag

try:
	from TechParser import flowa
except ImportError:
	import flowa

try:
	from TechParser import ittoolbox
except ImportError:
	import ittoolbox

try:
	from TechParser import dzone
except ImportError:
	import dzone

try:
	from TechParser import codeproject
except ImportError:
	import codeproject

try:
	from TechParser import hackernews
except ImportError:
	import hackernews

try:
	from TechParser import mashable
except ImportError:
	import mashable

try:
	from TechParser import maketecheasier
except ImportError:
	import maketecheasier

try:
	from TechParser import digg
except ImportError:
	import digg

try:
	from TechParser import wired
except ImportError:
	import wired

sites_to_parse = {
		"Habrahabr": { # habrahabr.ru
			"module": habrahabr,
			"kwargs": {}
		},
		
		"VentureBeat": { # venturebeat.com
			"module": venturebeat,
			"kwargs": {"start_page": 1, "end_page": 3}
		},
		
		"Engadget": { # engadget.com
			"module": engadget,
			"kwargs": {"start_page": 1, "end_page": 5}
		},
		
		"Slashdot": { # slashdot.org
			"module": slashdot,
			"kwargs": {"start_page": 1, "end_page": 3}
		},
		
		"Gizmodo": { # gizmodo.com
			"module": gizmodo,
			"kwargs": {}
		},
		
		"TechCrunch": { # techcrunch.com
			"module": techcrunch,
			"kwargs": {}
		},
		
		# Works only with Selenium (opens REAL browser)
		#"Read/Write Web": { # readwrite.com
		#	"module": readwrite,
		#	"kwargs": {"browser": "firefox"}
		#},
		
		"Tech Republic": { # techrepublic.com
			"module": techrepublic,
			"kwargs": {}
		},
		
		"Smashing Magazine": { # www.smashingmagazine.com
			"module": smashingmagazine,
			"kwargs": {}
		},
		
		"Android Central": { # www.androidcentral.com
			"module": androidcentral,
			"kwargs": {"start_page": 1, "end_page": 5}
		},
		
		"The Verge": { # www.theverge.com
			"module": verge,
			"kwargs": {}
		},
		
		"Top Design Magazine": { # www.topdesignmag.com
			"module": topdesignmag,
			"kwargs": {"start_page": 1, "end_page": 1}
		},
		
		"Flowa": { # flowa.fi
			"module": flowa,
			"kwargs": {}
		},
		
		"IT Toolbox": { # it.toolbox.com
			"module": ittoolbox,
			"kwargs": {}
		},
		
		"DZone": { # www.dzone.com
			"module": dzone,
			"kwargs": {}
		},
		
		"Code Project": { # www.codeproject.com
			"module": codeproject,
			"kwargs": {"start_page": 1, "end_page": 1}
		},
		
		"Hacker News": { # news.ycombinator.com/newest
			"module": hackernews,
			"kwargs": {"start_page": 1, "end_page": 5}
		},
		
		"Mashable": { # mashable.com
			"module": mashable,
			"kwargs": {}
		},
		
		"Make Tech Easier": { # www.maketecheasier.com
			"module": maketecheasier,
			"kwargs": {}
		},
		
		"Digg": { # digg.com
			"module": digg,
			"kwargs": {}
		},
		
		"Wired": { # www.wired.com
			"module": wired,
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

save_articles = False # Save articles into db.
# Can be found at ~/.tech-parser/archive.db
