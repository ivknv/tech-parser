#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser.parsers import *

sites_to_parse = {
	"Habrahabr": { # habrahabr.ru
		"module": habrahabr,
		"kwargs": {"hubs": []},
		"enabled": True
	},
	
	"VentureBeat": { # venturebeat.com
		"module": venturebeat,
		"kwargs": {},
		"enabled": True
	},
	
	"Engadget": { # engadget.com
		"module": engadget,
		"kwargs": {},
		"enabled": True
	},
	
	"Slashdot": { # slashdot.org
		"module": slashdot,
		"kwargs": {},
		"enabled": True
	},
	
	"Gizmodo": { # gizmodo.com
		"module": gizmodo,
		"kwargs": {},
		"enabled": True
	},
	
	"TechCrunch": { # techcrunch.com
		"module": techcrunch,
		"kwargs": {},
		"enabled": True
	},
	
	"Read/Write Web": { # readwrite.com
		"module": readwrite,
		"kwargs": {},
		"enabled": True
	},
	
	"Tech Republic": { # techrepublic.com
		"module": techrepublic,
		"kwargs": {},
		"enabled": True
	},
	
	"Smashing Magazine": { # www.smashingmagazine.com
		"module": smashingmagazine,
		"kwargs": {},
		"enabled": True
	},
	
	"Android Central": { # www.androidcentral.com
		"module": androidcentral,
		"kwargs": {},
		"enabled": True
	},
	
	"The Verge": { # www.theverge.com
		"module": verge,
		"kwargs": {},
		"enabled": True
	},
	
	"Top Design Magazine": { # www.topdesignmag.com
		"module": topdesignmag,
		"kwargs": {},
		"enabled": True
	},
	
	"Flowa": { # flowa.fi
		"module": flowa,
		"kwargs": {},
		"enabled": True
	},
	
	"IT Toolbox": { # it.toolbox.com
		"module": ittoolbox,
		"kwargs": {},
		"enabled": True
	},
	
	"DZone": { # www.dzone.com
		"module": dzone,
		"kwargs": {},
		"enabled": True
	},
	
	"Code Project": { # www.codeproject.com
		"module": codeproject,
		"kwargs": {'categories': ['all']}, # 'web', 'android', 'c#', 'c++' and 'ios'
		"enabled": True
	},
	
	"Hacker News": { # news.ycombinator.com
		"module": hackernews,
		"kwargs": {},
		"enabled": True
	},
	
	"Mashable": { # mashable.com
		"module": mashable,
		"kwargs": {},
		"enabled": True
	},
	
	"Make Tech Easier": { # www.maketecheasier.com
		"module": maketecheasier,
		"kwargs": {},
		"enabled": True
	},
	
	"Digg": { # digg.com
		"module": digg,
		"kwargs": {},
		"enabled": True
	},
	
	"Wired": { # www.wired.com
		"module": wired,
		"kwargs": {},
		"enabled": True
	},
	
	"Medium": { # medium.com
		"module": medium,
		"kwargs": {"collections": []},
		"enabled": True
	},
	
	"Planet Clojure": { # planet.clojure.in
		"module": planetclojure,
		"kwargs": {},
		"enabled": True
	},
	
	"Reddit": { # www.reddit.com
		"module": reddit,
		"kwargs": {"reddits": ["tech"]},
		"enabled": True
	},
	
	"Trashbox": { # trashbox.ru
		"module": trashbox,
		# all, articles, news, main_page, games, programs, themes, questions
		"kwargs": {'categories': ['all']},
		"enabled": True
	},
	
	"Droider": { # droider.ru
		"module": droider,
		"kwargs": {},
		"enabled": True
	},
	
	"Redroid": { # redroid.ru
		"module": redroid,
		"kwargs": {},
		"enabled": True
	},
	
	"3DNews": { # www.3dnews.ru
		"module": threednews,
		"kwargs": {},
		"enabled": True
	},
		
	"IXBT": { # www.ixbt.ru
		"module": ixbt,
		"kwargs": {},
		"enabled": True
	},
	
	"Mobile Review": { # mobile-review.com
		"module": mobilereview,
		"kwargs": {},
		"enabled": True
	},
	
	"Helpix": { # helpix.ru
		"module": helpix,
		"kwargs": {},
		"enabled": True
	},
	
	"Re/code": { # recode.net
		"module": recode,
		"kwargs": {},
		"enabled": True
	},
	
	"ZDNet": { # www.zdnet.com
		"module": zdnet,
		"kwargs": {'categories': ['all']}, # 'news', 'reviews' and 'downloads',
		"enabled": True
	},
		
	"Geektimes": { # geektimes.ru
		"module": geektimes,
		"kwargs": {'hubs': []},
		"enabled": True
	}
}

# RSS feeds
rss_feeds = {
	# 'Feed name': {
	#	'short-name': 'feed-name',
	#	'icon': 'http://<address-to-feed>.com/<address-to-feed-icon>',
	#	'color': '#123ABC' # CSS color for titles
	#	'enabled': True # or False to disable
	#}
}

# Words that you're interested in
interesting_words = []

# Words that you find boring
boring_words = []

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

# Environment variable that stores path to archive database
archive_db_path_variable = 'ARCHIVE_DATABASE_URL'

# Should look like 'sqlite:///PATH' or 'postgres://user:password@host:port/dbname'
# 'default' means 'sqlite:///<your-home-directory>/.tech-parser/archive.db'
archive_db_path = os.environ.get(archive_db_path_variable, 'default')

# Format to be used when dumping articles.
# Can be 'pickle', 'json' or 'db'.
# It's recommended to set data_format to 'db' (database) because it's a lot faster.
# Pickle is set by default for compatibility with previous versions of TechParser
data_format = 'pickle'

# Environment variable to keep your password
password_variable = 'TechParser_PASSWORD'

# Password
password = os.environ.get(password_variable, '')

# Show Pocket button under every article.
# Disabled by default because it slows down page loading.
# Besides, you can save links to Pocket with a plugin for your browser.
enable_pocket = False

# If json_config is set to True it will allow you to edit configuration in your browser
json_config = True
