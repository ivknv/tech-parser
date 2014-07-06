tech-parser
===========

Parses articles from 11 sites and outputs it into HTML.

Current list of sites:
<ol>
	<li>habrahabr.ru</li>
	<li>venturebeat.com</li>
	<li>engadget.com</li>
	<li>techrepublic.com</li>
	<li>techcrunch.com</li>
	<li>smashingmagazine.com</li>
	<li>theverge.com</li>
	<li>slashdot.org</li>
	<li>gizmodo.com</li>
	<li>androidcentral.com</li>
	<li>readwrite.com</li>
</ol>

## Requirements ##
Django (for pagination)<br/>
mako<br/>
bottle<br/>
lxml<br/>
grab<br/>

## How to use ##
```python main.py```<br/>
And then open localhost:8080 in your browser.

## Configuring ##
### Enabling/disabling parsers ###
To enable/disable site parsers edit ```parser_config.py```<br/>
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

For example if ```update_interval``` will be set to ```3600```, it will update data every 30 minutes.


### Custom host and port ###
In ```parser_config.py``` find two variables: ```host``` and ```port``` and set them equal to whatever hsot and port you want
