#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime

from mako.lookup import TemplateLookup
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

def filter_articles(articles):
    """Filter articles"""
    
    config = get_conf.config
    
    articles_filtered = OrderedDict()
    
    for article in articles.values():
        passing = True
        
        words_len = len(config.filters["All"]["or"])
        title = article["title"].lower()
        
        for word in config.filters["All"]["or"]:
            if word.lower() in title:
                passing = True
                break
            else:
                words_len -= 1
            
            if words_len == 0:
                passing = False
                
        if passing:
            for word in config.filters["All"]["not"]:
                if word.lower() in title:
                    passing = False
                    break
        if passing: 
            for word in config.filters["All"]["has"]:
                if word.lower() not in title:
                    passing = False
                    break
        if passing:
            articles_filtered[article['link']] = article
    
    return articles_filtered

def load_articles(filename="articles_dumped"):
    """Load articles from ~/.tech-parser/<filename>"""
    
    try:
        return save.load_from_file(os.path.join(logdir, filename))
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
    
    try:
        articles = load_articles()
    except IOError:
        dump_articles()
        articles = load_articles()
    
    articles = filter_articles(articles)
    if q:
        qs = q.lower().split()
        articles = filter(lambda x: has_words(qs, x), articles.values())
        articles = map(lambda x: escape_link(x), articles)
    else:
        articles = map(lambda x: escape_link(x), articles.values())
    all_articles = articles
    articles = split_into_pages(articles, 30)
    try:
        requested_page = articles[page_number-1]
        set_liked(requested_page)
    except IndexError:
        requested_page = []
    
    return main_page.render(articles=requested_page,
        num_pages=len(articles),
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
    template = mylookup.get_template('edit.html')
    config = get_conf.Config.from_module(get_conf.config)
    config.interesting_words = json.dumps(config.interesting_words, ensure_ascii=False)
    config.boring_words = json.dumps(config.boring_words, ensure_ascii=False)
    config.filters = json.dumps(config.filters, ensure_ascii=False)
    for parser in config.sites_to_parse.values():
        parser['kwargs'] = json.dumps(parser['kwargs'])
    
    return template.render(config=config,
        page='edit', q='')

@route('/update/', method='POST')
@login_required
def update_config():
    type_ = request.POST.getunicode('type')
    
    if type_ == 'variables':
        update_interval = request.POST.getunicode('v_update_interval', get_conf.config.update_interval)
        db = request.POST.getunicode('v_db', get_conf.config.db)
        db_path_variable = request.POST.getunicode('v_db_path_var')
        if not db_path_variable:
            db_path = request.POST.getunicode('v_db_path', get_conf.config.db_path)
        else:
            db_path = None
        host = request.POST.getunicode('v_host', get_conf.config.host)
        port = request.POST.getunicode('v_port', get_conf.config.port)
        num_threads = request.POST.getunicode('v_num_threads', get_conf.config.num_threads)
        server = request.POST.getunicode('v_server', get_conf.config.server)
        save_articles = request.POST.getunicode('v_save_articles', False) == 'on'
        archive_db_path_variable = request.POST.getunicode('v_archive_db_path_var')
        if not archive_db_path_variable:
            archive_db_path = request.POST.getunicode('v_archive_db_path', get_conf.config.archive_db_path)
        else:
            arhcive_db_path = None
        data_format = request.POST.getunicode('v_data_format', get_conf.config.data_format)
        password_variable = request.POST.getunicode('v_password_var')
        if not password_variable:
            password = request.POST.getunicode('v_password', get_conf.config.password)
        else:
            password = None
        enable_pocket = request.POST.getunicode('v_enable_pocket', False) == 'on'
        
        redirect_path = '/edit#variables'
    elif type_ == 'parsers':
        for parser in get_conf.config.sites_to_parse.values():
            h = parser['hash']
            enabled = request.POST.getunicode('parser_{0}'.format(h)) in {'on', True}
            
            if enabled:
                kwargs = request.POST.getunicode('kwargs_{0}'.format(h), parser['kwargs'])
                parser['kwargs'] = json.loads(kwargs)
                parser['enabled'] = True
            else:
                parser['enabled'] = False
        redirect_path = '/edit#parsers'
    elif type_ == 'rss_feeds':
        to_delete = []
        for feed_name, feed in get_conf.config.rss_feeds.items():
            h = feed['hash']
            if request.POST.getunicode('is_deleted_{0}'.format(h), '0') == '1':
                to_delete.append(feed_name)
                continue
            name = request.POST.getunicode('name_{0}'.format(h), feed_name)
            short_name = request.POST.getunicode('sn_{0}'.format(h), feed['short-name'])
            url = request.POST.getunicode('url_{0}'.format(h), feed['url'])
            icon_url = request.POST.getunicode('icon_{0}'.format(h), feed['icon'])
            title_color = request.POST.getunicode('color_{0}'.format(h), feed['color'])
            enabled = request.POST.getunicode('enabled_{0}'.format(h), '0') == '1'
            
            feed['short-name'] = short_name
            feed['url'] = url
            feed['icon'] = icon_url
            feed['color'] = title_color
            feed['hash'] = hash(name)
            feed['enabled'] = enabled
            get_conf.config.rss_feeds[name] = feed
        for k in to_delete:
            get_conf.config.rss_feeds.pop(k)
        
        if request.POST.getunicode('new_feed', '1') == '1':
            new_feed_name = request.POST.getunicode('new_feed_name')
            new_feed_short_name = request.POST.getunicode('new_feed_sn')
            new_feed_url = request.POST.getunicode('new_feed_url')
            new_feed_icon = request.POST.getunicode('new_feed_icon')
            new_feed_color = request.POST.getunicode('new_feed_color')
            new_feed_enabled = request.POST.getunicode('new_feed_enabled', '0') == '1'
            if new_feed_name and new_feed_short_name and new_feed_url and new_feed_icon and new_feed_color:
                get_conf.config.rss_feeds[new_feed_name] = {'short-name': new_feed_short_name,
                                                            'url': new_feed_url,
                                                            'icon': new_feed_icon,
                                                            'color': new_feed_color,
                                                            'enabled': new_feed_enabled,
                                                            'hash': hash(new_feed_name)}
        
        redirect_path = '/edit#rss_feeds'
    elif type_ == 'interesting_words':
        iw = json.loads(request.POST.getunicode('t_interesting_words', '[]'), encoding='utf-8')
        get_conf.config.interesting_words = iw
        redirect_path = '/edit#interesting_words'
    elif type_ == 'boring_words':
        bw = json.loads(request.POST.getunicode('t_boring_words', '[]'), encoding='utf-8')
        get_conf.config.boring_words = bw
        redirect_path = '/edit#boring_words'
    elif type_ == 'filters':
        filters = json.loads(request.POST.getunicode('t_filters', '{"All": {"not": [], "or": [], "has": []}}'), encoding='utf-8')
        get_conf.config.filters = filters
        redirect_path = '/edit#filters'
    else:
        redirect_path = '/edit/'
    
    save.write_config(get_conf.config)
    redirect(redirect_path)
