tech-parser
===========

Parses articles from 15 sites and outputs it into HTML.

You can see it in action [here](http://tech-parser.herokuapp.com).
And [here's](https://github.com/SPython/web-tech-parser) repo for that Heroku app.

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
	<li>topdesignmag.com</li>
	<li>flowa.fi</li>
	<li>it.toolbox.com</li>
	<li>dzone.com</li>
	<li>codeproject.com</li>
</ol>

## Installation ##
### Requirements ###
Mako<br/>
Bottle<br/>
Grab<br/>
[Daemo](http://github.com/SPython/daemo.git)<br/>

All these modules can be installed with pip or easy_install.

### How to install ###
Run ```python setup.py install```.<br/>
And also, to make it easier to use I recommend to make an alias like this:<br/>
```alias tech-parser="python -m TechParser"``` on \*nix based OS or<br/>
```doskey tech-parser=python -m TechParser $*``` on Windows<br/>
After that You will be able to run  ```tech-parser``` instead of ```python -m TechParser```.

## How to use ##
Run ```python -m TechParser start``` to start server<br/>
And then open [localhost:8080](http://localhost:8080) in your browser.<br/>
```python -m TechParser stop``` to stop server<br/>
```python -m TechParser restart``` to restart server<br/>
```python -m TechParser update``` to manually update list of articles.<br/>
```python -m TechParser run HOST:PORT``` run server without starting daemon.<br/>
```python -m TechParser -h``` show help.

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
