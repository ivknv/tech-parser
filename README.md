tech-parser
===========

Parses articles from 34 sites and outputs it into HTML.
Also, it's some sort of RSS reader.

You can see it in action [here](http://tech-parser.herokuapp.com).
And [here's](https://github.com/SPython/web-tech-parser) repo for that Heroku app.

## Table of contents ##
<ol>
	<li><a href="#current-list-of-sites">Current list of sites</a></li>
	<li><a href="#one-awesome-feature">One awesome feature</a></li>
	<li><a href="#installation">Installation</a>
		<ul>
			<li><a href="#requirements">Requirements</a></li>
			<li><a href="#how-to-install">How to install</a></li>
		</ul>
	</li>
	<li><a href="#how-to-use">How to use</a></li>
	<li><a href="#configuring">Configuring</a>
		<ul>
			<li><a href="#enablingdisabling-parsers">Enabling/disabling parsers</a></li>
			<li><a href="#adding-rss-feeds">Adding RSS feeds</a></li>
			<li><a href="#asynchronous-parsing">Asynchronous parsing</a></li>
			<li><a href="#word-lists">Word lists</a></li>
			<li><a href="#filters">Filters</a>
				<ul>
					<li><a href="#examples">Examples</a></li>
				</ul>
			</li>
			<li><a href="#update-interval">Update interval</a></li>
			<li><a href="#custom-host-and-port">Custom host and port</a></li>
		</ul>
	</li>
</ol>

## Current list of sites ##
<ol>
	<li>habrahabr.ru (russian)</li>
	<li>venturebeat.com</li>
	<li>engadget.com</li>
	<li>techrepublic.com</li>
	<li>techcrunch.com</li>
	<li>smashingmagazine.com</li>
	<li>theverge.com</li>
	<li>slashdot.org</li>
	<li>gizmodo.com</li>
	<li>androidcentral.com</li>
	<li>topdesignmag.com</li>
	<li>flowa.fi</li>
	<li>it.toolbox.com</li>
	<li>dzone.com</li>
	<li>codeproject.com</li>
	<li>news.ycombinator.com</li>
	<li>mashable.com</li>
	<li>maketecheasier.com</li>
	<li>digg.com</li>
	<li>wired.com</li>
	<li>medium.com</li>
	<li>planet.clojure.in</li>
	<li>reddit.com</li>
	<li>mobile-review.com (russian)</li>
	<li>ixbt.ru (russian)</li>
	<li>readwrite.com</li>
	<li>trashbox.ru (russian)</li>
	<li>droider.ru (russian)</li>
	<li>redroid.ru (russian)</li>
	<li>3dnews.ru (russian)</li>
	<li>helpix.ru (russian)</li>
	<li>recode.net</li>
	<li>zdnet.com</li>
	<li>geektimes.ru (russian)</li>
</ol>

## One awesome feature ##
Before You scroll away, I want You to know about one awesome feature that TechParser has.<br/>
I'm talking about ranking.<br/><br/>
Every time when You click on like button below article TechParser adds it to the database.<br/>
And next time when it will parse articles it will sort them according to those articles in that database.

## Installation ##
### Requirements ###
Mako<br/>
Bottle<br/>
Grab<br/>
[Daemo](http://github.com/SPython/daemo.git)<br/>

All these modules can be installed with pip or easy_install.

### How to install ###
You can install TechParser by running<br/>
```pip install TechParser```<br/> or<br/>
```python setup.py install```<br/>
And also, to make it easier to use I recommend to make an alias like this:<br/>
```alias tech-parser="python -m TechParser"``` on \*nix based OS or<br/>
```doskey tech-parser=python -m TechParser $*``` on Windows<br/>
After that You will be able to run  ```tech-parser``` instead of ```python -m TechParser```.

## How to use ##
Run ```python -m TechParser start``` to start server<br/>
And then open [localhost:8080](http://localhost:8080) in your browser.<br/>
```python -m TechParser stop``` to stop server<br/>
```python -m TechParser update``` to manually update list of articles.<br/>
```python -m TechParser run HOST:PORT``` run server without starting daemon.<br/>
```python -m TechParser -h``` show help.<br/>
```python -m TechParser <action> --config <path to configuration file>``` set path to configuration file.

## Configuring ##
### Enabling/disabling parsers ###
To enable/disable site parsers edit ```~/.tech-parser/user_parser_config.py```.<br/>
If you can't find the file, run ```python -m TechParser``` then search again.<br/>
Find there line with ```sites_to_parse``` and comment those sites, which you don't want to see articles from.<br/>

For example if you don't want to see articles from Habrahabr (it's in russian only), find this fragment of code:

```python
		"Habrahabr": {
			"link": "habrahabr.ru",
			"module": habrahabr,
			"kwargs": {}
		},
```

and make it look like this:

```python
		#"Habrahabr": {
		#	"link": "habrahabr.ru",
		#	"module": habrahabr,
		#	"kwargs": {}
		#},
```

### Adding RSS feeds ###
Find the following line in your configuration:
```python
rss_feeds = {}
```

RSS feed should contain it's name, url, short name (without spaces and stuff like that), url to icon and title color.
Example feeds:
```python
rss_feeds = {'CSS-tricks': {
		'short-name': 'css-tricks',
		'url': 'http://feeds.feedburner.com/CssTricks?format=xml',
		'icon': 'http://css-tricks.com/favicon.ico',
		'color': '#DA8817'
	},
	
	'The Next Web':	{
		'url': 'http://feeds2.feedburner.com/thenextweb',
		'short-name': 'nextweb',
		'icon': 'http://thenextweb.com/favicon.ico',
		'color': '#F15A2F'
	}
}
```

### Asynchronous parsing ###
You can set number of threads available for parsing.<br/>
To do that you need to set ```num_threads``` in your configuration.<br/>
Example:
```python
num_threads = 4
```

### Word lists ###
Articles can also be sorted by words you find interesting and boring.
To do that you can set variables ```interesting_words``` and ```boring_words```.
Example:
```python
interestring_words = {'word1', 'word2', 'word3'}
boring_words = {'word4', 'word5', 'word6'}
```

You can also set priority for each word:
```python
interesting_words = {('python', 5.0), ('fortran', 3.0), 'css', 'html', ('google', 1.5)}
boring_words = {('pascal', 10.0), 'delphi'}
```

Default priority for each word is ```1```

### Filters ###
Find fragment of code like this:
```python
filters = {
	"All": {
		"has": [],
		"or": [],
		"not": []
	}
}
```

```has```: title has all of these words<br/>
```or```: title has some of these words<br/>
```not```: title doesn't have any of these words<br/>

#### Examples ####
articles, containing words "google" and "android", but not containing "apple":
```python
filters = {
	"All": {
		"has": ["google", "android"],
		"or": [],
		"not": ["apple"]
	}
}
```

Articles, containing words "htc" or "android l":
```python
filters = {
	"All": {
		"has": [],
		"or": ["htc", "android l"],
		"not": []
	}
}
```

### Update interval ###
Find the line of code in ```parser_config.py``` like this:

```python
update_interval = 1800
```

and set ```update_interval``` equal to any amount of seconds you want.<br/>

For example if ```update_interval``` will be set to ```3600```, it will update data every hour.<br/>
Note that __this hour is not hour after server start.__<br/>
It means, that every time, when epoch time is divisible by ```3600``` TechParser will update articles.
With this interval TechParser will update articles at:<br/>
00:00<br/>
01:00<br/>
02:00<br/>
...<br/>
13:00<br/>
14:00<br/>
...and so on.


### Custom host and port ###
In ```~/.tech-parser/user_parser_config.py``` find two variables: ```host``` and ```port``` and set them equal to whatever host and port you want.<br/>
Example:
```python
host="0.0.0.0"
port="8081"
```
