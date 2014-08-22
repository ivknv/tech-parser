#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import habrahabr
from TechParser import venturebeat
from TechParser import engadget
from TechParser import techcrunch
from TechParser import techrepublic
#from TechParser import readwrite
from TechParser import smashingmagazine
from TechParser import gizmodo
from TechParser import slashdot
from TechParser import androidcentral
from TechParser import verge
from TechParser import topdesignmag
from TechParser import flowa
from TechParser import ittoolbox
from TechParser import dzone
from TechParser import codeproject
from TechParser import hackernews
from TechParser import mashable
from TechParser import maketecheasier
from TechParser import digg
from TechParser import wired
from TechParser import medium
from TechParser import planetclojure
from TechParser import reddit

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
		},
		
		"Medium": { # medium.com
			"module": medium,
			"kwargs": {"collections": []}
		},
		
		"Planet Clojure": { # planet.clojure.in
			"module": planetclojure,
			"kwargs": {}
		},
		
		"Reddit": { # www.reddit.com
			"module": reddit,
			"kwargs": {"reddits": ["tech"]}
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
