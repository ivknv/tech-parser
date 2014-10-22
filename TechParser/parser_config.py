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
from TechParser import trashbox
from TechParser import droider
from TechParser import redroid
from TechParser import threednews
from TechParser import ixbt
from TechParser import mobilereview
from TechParser import helpix
from TechParser import recode
from TechParser import zdnet
from TechParser import geektimes

sites_to_parse = {
	"Habrahabr": { # habrahabr.ru
		"module": habrahabr,
		"kwargs": {"hubs": []}
	},
	
	"VentureBeat": { # venturebeat.com
		"module": venturebeat,
		"kwargs": {}
	},
	
	"Engadget": { # engadget.com
		"module": engadget,
		"kwargs": {}
	},
	
	"Slashdot": { # slashdot.org
		"module": slashdot,
		"kwargs": {}
	},
	
	"Gizmodo": { # gizmodo.com
		"module": gizmodo,
		"kwargs": {}
	},
	
	"TechCrunch": { # techcrunch.com
		"module": techcrunch,
		"kwargs": {}
	},
	
	"Read/Write Web": { # readwrite.com
		"module": readwrite,
		"kwargs": {"browser": "firefox"}
	},
	
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
		"kwargs": {}
	},
	
	"The Verge": { # www.theverge.com
		"module": verge,
		"kwargs": {}
	},
	
	"Top Design Magazine": { # www.topdesignmag.com
		"module": topdesignmag,
		"kwargs": {}
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
		"kwargs": {'categories': ['all']}
	},
	
	"Hacker News": { # news.ycombinator.com
		"module": hackernews,
		"kwargs": {}
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
	},
	
	"Trashbox": { # trashbox.ru
		"module": trashbox,
		"kwargs": {}
	},
	
	"Droider": { # droider.ru
		"module": droider,
		"kwargs": {}
	},
	
	"Redroid": { # redroid.ru
		"module": redroid,
		"kwargs": {}
	},
	
	"3DNews": { # www.3dnews.ru
		"module": threednews,
		"kwargs": {}
	},
		
	"IXBT": { # www.ixbt.ru
		"module": ixbt,
		"kwargs": {}
	},
	
	"Mobile Review": { # mobile-review.com
		"module": mobilereview,
		"kwargs": {}
	},
	
	"Helpix": { # helpix.ru
		"module": helpix,
		"kwargs": {}
	},
	
	"Re/code": { # recode.net
		"module": recode,
		"kwargs": {}
	},
	
	"ZDNet": { # www.zdnet.com
		"module": zdnet,
		"kwargs": {}
	},
		
	"Geektimes": { # geektimes.ru
		"module": geektimes,
		"kwargs": {'hubs': []}
	}
}

rss_feeds = {}

filters = {
	"All": {
		"has": [],
		"or": [],
		"not": []
	}
}

update_interval = 1800 # Parse articles every 30 minutes

# Database for keeping history
# must be sqlite or postgresql.
# If You're using postgresql make sure
# to set environment variable DATABASE_URL
# like this: postgres://user:password@host:port/dbname
db = 'sqlite'
host = "0.0.0.0" # Server host
port = "8080" # Server port

num_threads = 2 # Number of threads for parsing articles

# Server to use
# It's recommended to use tornado.
# You can install it by running pip install tornado
server = "auto" # See http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend

save_articles = False # Save articles into db.
# Can be found at ~/.tech-parser/archive.db
