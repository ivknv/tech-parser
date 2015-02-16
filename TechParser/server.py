#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime

from mako.lookup import TemplateLookup
import bottle
from bottle import route, run, static_file, request, redirect, response
from collections import OrderedDict

from TechParser import get_conf, recommend, save
from TechParser.db_functions import *
from TechParser.py2x import unicode_, unicode__, range, urlencode, pickle, parse_qs

module_path = os.path.dirname(os.path.realpath(__file__))
template_dir_path = os.path.join(module_path, "templates")
static_dir_path = os.path.join(module_path, "static")
logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

mylookup = TemplateLookup(directories=template_dir_path,
                          default_filters=["decode.utf8"],
                          input_encoding="utf-8", output_encoding="utf-8")

liked = []
disliked = []
liked_links = []
disliked_links = []
errors = {}

CSS_NAME_REGEX = re.compile(r'-?[_a-zA-Z]+[_a-zA-Z0-9-]*$')

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.items():
        if isinstance(v, unicode__):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

def remove_tags(s):
    return recommend.r0.sub('', s)

def split_into_pages(articles, n=30):
    """Split list into pages"""
    
    pages = []
    i = 0
    
    for j in articles:
        if i >= n:
            i = 0
        
        if i == 0:
            pages.append([j])
        else:
            pages[-1].append(j)
        
        i += 1
    
    return pages

def get_sid():
    return request.get_cookie('sid', '')

def logged_in():
    password = not len(get_conf.config.password)
    return check_session_existance(get_sid()) or password

def encode_url(url):
    return urlencode(encoded_dict({'': url}))[1:]

def login_required(func):
    def newfunc(*args, **kwargs):
        if logged_in():
            return func(*args, **kwargs)
        redirect('/login/?return_to={0}'.format(encode_url(request.path)))
    return newfunc

class Validator(object):
    def __init__(self):
        self.errors = {}
    
    def add_error(self, location, msg):
        """Add error to error list"""
        
        self.errors.setdefault(location, [])
        self.errors[location].append(msg)
    
    def validate(self, **data):
        """Validate configuration"""
        
        if data['type'] == 'variables':
            # Validate variables
            try:
                update_interval = int(data['update_interval'])
                if update_interval <= 0:
                    self.add_error('update_interval', 'update_interval should be bigger than 0')
            except ValueError:
                self.add_error('update_interval', 'Update interval should be a number')
            if data['db'] not in {'sqlite', 'postgresql'}:
                self.add_error('db', 'Database should be either sqlite or postgresql')
            try:
                num_threads = int(data['num_threads'])
                if num_threads < 1:
                    self.add_error('num_threads', 'Number of threads should be more than 0')
                if num_threads > 10:
                    self.add_error('num_threads', 'Maximum number of threads is 10')
            except ValueError:
                self.add_error('num_threads', 'Number of threads should be an integer between 1 and 10')
            
            if data['server'] not in bottle.server_names:
                servers = map(lambda x: '<a href="javascript:void(0)" onclick="$(\'input[name=v_server]\').val($(this).text())">{0}</a>'.format(x), bottle.server_names)
                self.add_error('server', 'Server must be one of these: {0}'.format(', '.join(servers)))
            try:
                port = int(data['port'])
                if port > 65535 or port < 1:
                    self.add_error('port', 'Port should be an integer between 1 and 65535')
            except ValueError:
                self.add_error('port', 'Port should be an integer')
            
            if data['data_format'] not in {'json', 'pickle', 'db'}:
                self.add_error('data_format', "data_format should be 'json', 'pickle' or 'db'")
        elif data['type'] == 'rss_feeds':
            feed = data['rss_feed']
            feed_name = data['rss_feed_name']
            h = feed['hash']
            location = 'rss_feed_{0}'.format(h)
            if not len(feed_name):
                self.add_error(location, 'Feed name cannot be empty')
            if not len(feed['short-name']):
                self.add_error(location, 'Feed short name cannot be empty')
            if not feed['url'].startswith('http://') and not feed['url'].startswith('https://'):
                self.add_error(location, 'Invalid URL')
            if not feed['icon'].startswith('http://') and not feed['icon'].startswith('https://'):
                 self.add_error(location, 'Invalid icon URL')
            if not CSS_NAME_REGEX.match(feed['short-name']):
                self.add_error(location, 'Short name must be a valid CSS name')

        return self.errors

def load_articles(filename="articles_dumped"):
    """Load articles from ~/.tech-parser/<filename>"""
    
    try:
        return save.load_from_somewhere(os.path.join(logdir, filename))
    except (IOError, pickle.PickleError, TypeError):
        return OrderedDict()

@route('/static/<filename:path>')
def serve_static(filename):
    """Serve static files"""
    
    return static_file(filename, root=static_dir_path)

def update_liked_disliked():
    global liked, disliked, liked_links, disliked_links

    config = get_conf.config
    
    liked = recommend.get_interesting_articles()
    disliked = recommend.get_blacklist()
    liked_links = [i['link'] for i in liked]
    disliked_links = [i['link'] for i in disliked]

@route('/histadd/<addr:path>')
@login_required
def add_to_history(addr):
    
    recommend.add_article(addr)
    
    update_liked_disliked()
    
@route('/blacklistadd/<addr:path>')
@login_required
def add_to_blacklist(addr):
    recommend.add_article_to_blacklist(addr)
    
    update_liked_disliked()

@route('/blacklistrm/<addr:path>')
@login_required
def rm_from_blacklist(addr):
    recommend.remove_from_blacklist(addr)
    
    update_liked_disliked()

@route('/histrm/<addr:path>')
@login_required
def rm_from_history(addr):
    recommend.remove_from_history(addr)
    
    update_liked_disliked()

@route('/history')
@route('/history/<page_number>')
@login_required
def show_history(page_number=1):
    history_page = mylookup.get_template('history.html')
    q = unicode_(request.GET.getunicode('q', ''))
    
    articles = recommend.get_interesting_articles()
    
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1
    
    if q:
        qs = q.lower().split()
        articles = filter(lambda x: has_words(qs, x), articles)
    
    articles = map(lambda x: escape_link(x), articles)
    
    all_articles = articles
    articles = split_into_pages(articles, 30)
    try:
        requested_page = articles[page_number-1]
    except IndexError:
        requested_page = []
    
    return history_page.render(articles=requested_page,
        num_pages=len(articles),
        page_num=page_number,
        q=q, page='history',
        config=get_conf.config)

@route('/blacklist')
@route('/blacklist/<page_number>')
@login_required
def show_blacklist(page_number=1):
    blacklist_page = mylookup.get_template('blacklist.html')
    q = unicode_(request.GET.getunicode('q', ''))
    
    articles = recommend.get_blacklist()
    
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1
    
    if q:
        qs = q.lower().split()
        articles = filter(lambda x: has_words(qs, x), articles)
    
    articles = map(lambda x: escape_link(x), articles)
    
    all_articles = articles
    articles = split_into_pages(articles, 30)
    try:
        requested_page = articles[page_number-1]
    except IndexError:
        requested_page = []
    
    return blacklist_page.render(articles=requested_page,
        num_pages=len(articles),
        page_num=page_number,
        q=q, page='blacklist',
        config=get_conf.config)

def has_words(qs, article):
    """Check if article contains words"""
    
    title = remove_tags(unicode_(article['title']).lower())
    summary = remove_tags(unicode_(article['summary']).lower())
    
    for i in qs:
        if i not in title and i not in summary:
            return False
    return True

def escape_link(article):
    """Escape HTML tags, etc."""
    
    new_article = {}
    new_article.update(article)
    new_article['original_link'] = new_article['link']
    
    new_article['link'] = encode_url(new_article['link'])
    return new_article

def set_liked(articles):
    for article in articles:
        article['liked'] = article['original_link'] in liked_links
        article['disliked'] = article['original_link'] in disliked_links

@route("/")
@route("/<page_number>")
@login_required
def article_list(page_number=1):
    """Show list of articles | Search for articles"""
    
    main_page = mylookup.get_template("articles.html")
    q = unicode_(request.GET.getunicode('q', ''))
    
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1
    
    if get_conf.config.data_format == 'db':
        if q:
            articles = select_all_articles()
            qs = q.lower().split()
            articles = filter(lambda x: has_words(qs, x), articles.values())
            articles = map(lambda x: escape_link(x), articles)
            articles = split_into_pages(articles, 30)
            num_pages = len(articles)
            try:
                requested_page = articles[page_number-1]
            except IndexError:
                requested_page = []
        else:
            requested_page = select_articles_from_page(page_number)
            requested_page = list(map(lambda x: escape_link(x), requested_page.values()))
            num_pages = int(get_var('num_pages', 1))
    else:
        try:
            articles = load_articles()
        except IOError:
            dump_articles()
            articles = load_articles()
    
        if q:
            qs = q.lower().split()
            articles = filter(lambda x: has_words(qs, x), articles.values())
            articles = map(lambda x: escape_link(x), articles)
        else:
            articles = map(lambda x: escape_link(x), articles.values())
     
        articles = split_into_pages(articles, 30)
        num_pages = len(articles)
        try:
            requested_page = articles[page_number-1]
        except IndexError:
            requested_page = []
    
    set_liked(requested_page)
    
    return main_page.render(articles=requested_page,
        num_pages=num_pages,
        page_num=page_number,
        q=q, page='main',
        config=get_conf.config,
        is_parsing=get_var('parsing', '0') == '1')

@route('/login')
@route('/login/')
@route('/login/', method='POST')
def login():
    ret = request.GET.getunicode('return_to', '/')
    if logged_in():
        redirect(ret)
    else:
        password = request.POST.getunicode('password', None)
        if password is not None and check_password(password):
            new_sid = add_session()
            now = datetime.datetime.now()
            expiration_date = datetime.datetime(now.year+1, now.month,
                now.day, now.hour, now.minute, now.second, now.microsecond)
            response.set_cookie('sid', new_sid, path='/',
                expires=expiration_date)
            redirect(ret)
        else:
            template = mylookup.get_template('login.html')
            return template.render(return_path=encode_url(ret),
                error=password is not None)

@route('/logout')
@route('/logout/')
def logout():
    if not logged_in():
        redirect('/login/')
    else:
        remove_session(get_sid())
        response.set_cookie('sid', '', expires=datetime.datetime(1970, 1, 1, 0, 0, 0))
        redirect('/login/')

@route('/edit')
@route('/edit/')
@login_required
def edit_config():
    global errors
    
    template = mylookup.get_template('edit.html')
    config = get_conf.Config.from_module(get_conf.config)
    config.interesting_words = json.dumps(config.interesting_words, ensure_ascii=False)
    config.boring_words = json.dumps(config.boring_words, ensure_ascii=False)
    
    for parser in config.sites_to_parse.values():
        parser['kwargs'] = json.dumps(parser['kwargs'])
    dup_errors = errors
    errors = {}
    
    return template.render(config=config, page='edit', q='',
                           errors=dup_errors)

def asserte(cond, msg):
    if not cond:
        errors[msg[0]] = errors.get(msg[0], []) + [msg[1]]

def try_asserte(value, func, msg):
    try:
        return func(value)
    except:
        errors[msg[0]] = errors.get(msg[0], []) + [msg[1]]

@route('/update/', method='POST')
@login_required
def update_config():
    type_ = request.POST.getunicode('type')
    validator = Validator()
    response = {}
    
    if type_ == 'variables':
        data = {}
        data['update_interval'] = request.POST.getunicode('v_update_interval', get_conf.config.update_interval)
        
        data['db'] = request.POST.getunicode('v_db', get_conf.config.db)
        data['db_path_variable'] = request.POST.getunicode('v_db_path_var')
        data['db_path'] = request.POST.getunicode('v_db_path', get_conf.config.db_path)
        
        data['host'] = request.POST.getunicode('v_host', get_conf.config.host)
        data['port'] = request.POST.getunicode('v_port', get_conf.config.port)
        
        data['num_threads'] = request.POST.getunicode('v_num_threads', get_conf.config.num_threads)
        
        data['server'] = request.POST.getunicode('v_server', get_conf.config.server)
        
        data['save_articles'] = request.POST.getunicode('v_save_articles', False) == 'on'
        
        data['archive_db_path_variable'] = request.POST.getunicode('v_archive_db_path_var')
        data['archive_db_path'] = request.POST.getunicode('v_archive_db_path', get_conf.config.archive_db_path)
        
        data['data_format'] = request.POST.getunicode('v_data_format', get_conf.config.data_format)
        
        data['password_variable'] = request.POST.getunicode('v_password_var')
        data['password'] = request.POST.getunicode('v_password', get_conf.config.password)
        
        data['enable_pocket'] = request.POST.getunicode('v_enable_pocket', False) == 'on'
        data['type'] = type_
        
        validator.validate(**data)
        
        if not validator.errors.get('update_interval'):
            get_conf.config.update_interval = int(data['update_interval'])
        if not validator.errors.get('db'):
            get_conf.config.db = data['db']
        get_conf.config.db_path_variable = data['db_path_variable']
        get_conf.config.db_path = data['db_path']
        get_conf.config.host = data['host']
        if not validator.errors.get('port'):
            get_conf.config.port = data['port']
        if not validator.errors.get('num_threads'):
            get_conf.config.num_threads = int(data['num_threads'])
        if not validator.errors.get('server'):
            get_conf.config.server = data['server']
        get_conf.config.archive_db_path_variable = data['archive_db_path_variable']
        get_conf.config.archive_db_path = data['archive_db_path']
        get_conf.config.data_format = data['data_format']
        get_conf.config.password_variable = data['password_variable']
        get_conf.config.password = data['password']
        get_conf.config.enable_pocket = data['enable_pocket'] 
    elif type_ == 'parsers':
        for parser in get_conf.config.sites_to_parse.values():
            h = parser['hash']
            enabled = request.POST.getunicode('parser_{0}'.format(h)) in {'on', True}
            
            if enabled:
                kwargs = request.POST.getunicode('kwargs_{0}'.format(h), parser['kwargs'])
                try:
                    parser['kwargs'] = json.loads(kwargs)
                except ValueError:
                    validator.add_error('parser_{0}'.format(h), 'Parser arguments should be in form of JSON')
                parser['enabled'] = True
            else:
                parser['enabled'] = False
    elif type_ == 'rss_feeds':
        response['deleted'], response['modified'] = [], []
        for feed_name, feed in get_conf.config.rss_feeds.items():
            h = feed['hash']
            data = {'rss_feed': {'hash': h}, 'type': type_}
            if request.POST.getunicode('is_deleted_{0}'.format(h), '0') == '1':
                response['deleted'].append((feed_name, h))
                continue
            data['rss_feed_name'] = request.POST.getunicode('name_{0}'.format(h), feed_name)
            data['rss_feed']['short-name'] = request.POST.getunicode('sn_{0}'.format(h), feed['short-name'])
            data['rss_feed']['url'] = request.POST.getunicode('url_{0}'.format(h), feed['url'])
            data['rss_feed']['icon'] = request.POST.getunicode('icon_{0}'.format(h), feed['icon'])
            data['rss_feed']['color'] = request.POST.getunicode('color_{0}'.format(h), feed['color'])
            data['rss_feed']['enabled'] = request.POST.getunicode('enabled_{0}'.format(h), '0') == '1'
            data['rss_feed']['hash'] = hash(data['rss_feed_name'])
            
            validator.validate(**data)
            
            if 'rss_feed_{0}'.format(h) not in validator.errors:
                rss_feed = data['rss_feed']
                short_name = rss_feed['short-name']
                name = data['rss_feed_name']
                url = rss_feed['url']
                icon = rss_feed['icon']
                color = rss_feed['color']
                enabled = rss_feed['enabled']
                new_hash = rss_feed['hash']
                if short_name != feed['short-name']:
                    response['modified'].append(('sn_{0}'.format(h), short_name))
                if name != feed_name:
                    response['modified'].append(('name_{0}'.format(h), name))
                if url != feed['url']:
                    response['modified'].append(('url_{0}'.format(h), url))
                if icon != feed['icon']:
                    response['modified'].append(('icon_{0}'.format(h), icon))
                if color != feed['color']:
                    response['modified'].append(('color_{0}'.format(h), color))
                if enabled != feed['enabled']:
                    response['modified'].append(('enabled_{0}'.format(h), enabled))
                if new_hash != h:
                    response['modified'].append(('hash_{0}'.format(h), new_hash))
                feed['short-name'] = short_name
                feed['url'] = url
                feed['icon'] = icon
                feed['color'] = color
                feed['enabled'] = enabled
                feed['hash'] = new_hash
                get_conf.config.rss_feeds[data['rss_feed_name']] = feed
                if data['rss_feed_name'] != feed_name:
                    get_conf.config.rss_feeds.pop(feed_name)
        for k in response['deleted']:
            get_conf.config.rss_feeds.pop(k[0])
        
        if request.POST.getunicode('new_feed', '1') == '0':
            data = {'rss_feed': {'hash': 'new_feed'}, 'type': 'rss_feeds'}
            data['rss_feed_name'] = request.POST.getunicode('new_feed_name')
            if data['rss_feed_name'] in get_conf.config.rss_feeds:
                validator.add_error('rss_feed_new_feed', 'RSS feed with such name already exists')
            data['rss_feed']['short-name'] = request.POST.getunicode('new_feed_sn')
            data['rss_feed']['url'] = request.POST.getunicode('new_feed_url')
            data['rss_feed']['icon'] = request.POST.getunicode('new_feed_icon')
            data['rss_feed']['color'] = request.POST.getunicode('new_feed_color')
            data['rss_feed']['enabled'] = request.POST.getunicode('new_feed_enabled', '0') == '1'
            validator.validate(**data)
            data['rss_feed']['hash'] = hash(data['rss_feed_name'])
            if 'rss_feed_new_feed' not in validator.errors:
                get_conf.config.rss_feeds[data['rss_feed_name']] = {'short-name': data['rss_feed']['short-name'],
                                                            'url': data['rss_feed']['url'],
                                                            'icon': data['rss_feed']['icon'],
                                                            'color': data['rss_feed']['color'],
                                                            'enabled': data['rss_feed']['enabled'],
                                                            'hash': data['rss_feed']['hash']}
                response['new_feed'] = data['rss_feed']
                response['new_feed']['name'] = data['rss_feed_name']
    elif type_ == 'interesting_words':
        try:
            get_conf.config.interesting_words = json.loads(request.POST.getunicode('t_interesting_words', '[]'), encoding='utf-8')
        except ValueError:
            validator.add_error('interesting_words', 'interesting_words should be a JSON object')
    elif type_ == 'boring_words':
        try:
            get_conf.config.boring_words = json.loads(request.POST.getunicode('t_boring_words', '[]'), encoding='utf-8')
        except ValueError:
            validator.add_error('boring_words', 'boring_words should be a JSON object')

    save.write_config(get_conf.config)
    response['errors'] = validator.errors
    
    return json.dumps(response)
