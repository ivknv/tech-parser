#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser.parsers import *

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
		"kwargs": {}
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
		"kwargs": {'categories': ['all']} # 'web', 'android', 'c#', 'c++' and 'ios'
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
		# all, articles, news, main_page, games, programs, themes, questions
		"kwargs": {'categories': ['all']}
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
		"kwargs": {'categories': ['all']} # 'news', 'reviews' and 'downloads'
	},
		
	"Geektimes": { # geektimes.ru
		"module": geektimes,
		"kwargs": {'hubs': []}
	}
}

# RSS feeds
rss_feeds = {
	# 'Feed name': {
	#	'short-name': 'feed-name',
	#	'icon': 'http://<address-to-feed>.com/<address-to-feed-icon>',
	#	'color': '#123ABC' # CSS color for titles
	#}
}

filters = {
	"All": {
		"has": [],
		"or": [],
		"not": []
	}
}

# Words that you're interested in
interesting_words = {}

# Words that you find boring
boring_words = {}

update_interval = 1800 # Parse articles every 30 minutes

# Database for keeping history
# Must be sqlite or postgresql
db = 'sqlite'
# If You're using PostgreSQL make sure
# to set database url as environment variable <db_path_variable>
# like this: postgres://user:password@host:port/dbname
# or just set db_path equal to that database url.
# Example 1:
#  db_path_variable = 'DATABASE_URL'
#  db_path = os.environ.get(db_path_variable)
# Example 2:
#  db_path_variable = 'DATABASE_URL'
#  db_path = postgres://user:password@localhost:5432/mydb
db_path_variable = 'DATABASE_URL'
db_path = os.environ.get(db_path_variable, '')
host = '0.0.0.0' # Server host
port = '8080' # Server port

num_threads = 2 # Number of threads for parsing articles

# Server to use
# It's recommended to use tornado.
# You can install it by running pip install tornado
# See http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend
server = "auto"

# Save articles to the database at <archive_db_path>.
save_articles = False
# Should look like 'sqlite:///PATH' or 'postgres://user:password@host:port/dbname'
# 'default' means 'sqlite:///<your-home-directory>/.tech-parser/archive.db'
archive_db_path = 'default'

# Format to be used when dumping articles.
# Can be 'pickle' or 'json'.
# JSON doesn't have problems with compatibility between 2.x and 3.x versions of Python so it's recommended.
# Pickle is default for compatibility with previous versions of TechParser
data_format = 'pickle'

# Password
password = os.environ.get('TechParser_PASSWORD', '')
