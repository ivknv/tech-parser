tech-parser
===========

Parses articles from 11 sites and outputs it into HTML

## Requirements ##
Django (for pagination)<br/>
mako<br/>
bottle<br/>
lxml<br/>
grab<br/>

## How to use ##
```python main.py```

## Configuring ##
To enable/disable parser edit ```parser_config.py```<br/>
Find there line with ```sites_to_parse``` and comment those sites, which you don't want to see articles from.<br/>
