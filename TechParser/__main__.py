#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
import os, sys, re, multiprocessing, argparse, sqlite3, atexit
from time import time, sleep

from mako.lookup import TemplateLookup
from bottle import route, run, static_file, default_app, request

from Daemo import Daemon, DaemonError

from TechParser import get_conf, recommend, parser
from TechParser.py2x import unicode_, unicode__, range, pickle, urlencode

if get_conf.config is None:
	get_conf.set_config_auto()

get_conf.auto_fix_config()

running_as_daemon = False

module_path = os.path.dirname(os.path.realpath(__file__))
template_dir_path = os.path.join(module_path, "templates")
static_dir_path = os.path.join(module_path, "static")
logdir = os.path.expanduser("~")
logdir = os.path.join(logdir, ".tech-parser")

if not os.path.exists(logdir):
	os.mkdir(logdir)

if not os.path.exists(os.path.join(logdir, "__init__.py")):
	open(os.path.join(logdir, "__init__.py"), "w").close()

if not os.path.exists(os.path.join(logdir, "user_parser_config.py")):
	f = open(os.path.join(logdir, "user_parser_config.py"), "w")
	default_config = open(os.path.join(module_path, "parser_config.py"))
	f.write(default_config.read())
	default_config.close()
	f.close()

mylookup = TemplateLookup(directories=template_dir_path,
	default_filters=["decode.utf8"],
	input_encoding="utf-8", output_encoding="utf-8")

liked = recommend.get_interesting_articles(db=get_conf.config.db)
disliked = recommend.get_blacklist(db=get_conf.config.db)
liked_links = [i['link'] for i in liked]
disliked_links = [i['link'] for i in disliked]

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

def setup_db():
	"""Setup archive database"""
	
	con = sqlite3.connect(os.path.join(logdir, "archive.db"))
	cur = con.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS articles
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT, link TEXT, source TEXT, UNIQUE(link));""")
	con.commit()
	con.close()

def log(text, f=sys.stdout, add_newline=True, clear_str=False,
	ignore_daemon=False):
	
	if add_newline:
		text += "\n"
	
	if (clear_str or running_as_daemon) and not ignore_daemon:
		text = re.sub(r"\033\[(\d+|\d+;\d+)m", "", text)
	
	f.write(text)
	f.flush()

def logerr(*args, **kwargs):
	kwargs['f'] = sys.stderr
	log(*args, **kwargs)

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

def simple_plural(n, s):
	n = str(n)
	if n.endswith("1") and not n.endswith("11"):
		return s
	else:
		return s + "s"

def show_progress(s, shared_object):
	progress = round(shared_object.value, 2)
	return "\033[0;32m[{0}%]\033[0m ".format(progress)+s

def parse_site(queue, articles, progress):
	config = get_conf.config
	
	while not queue.empty():
		site = queue.get()
		s = "Got {0} {1} from {2}"
		
		if site not in config.sites_to_parse:
			d = config.rss_feeds[site]
		else:
			d = config.sites_to_parse[site]
		
		update_progress(progress,
			100.0 / (len(config.sites_to_parse) + len(config.rss_feeds)) / 2.0)
		log(show_progress("Parsing articles from {0}".format(site), progress))
		
		if 'module' not in d:
			url = d.get('url', 'about:blank')
			short_name = d.get('short-name', 'unknown')
			icon = d.get('icon', 'about:blank')
			color = d.get('color', '#000')
			if not len(color):
				color = '#000'
			if not len(icon):
				icon = 'about:blank'
			
			try:
				new_articles = parser.parse_rss(url, short_name, icon, color)
				for i in new_articles:
					articles.put(i)
				update_progress(progress,
					100.0 / (len(config.sites_to_parse) + len(config.rss_feeds)) / 2.0)
				log(show_progress(s.format(len(new_articles),
					simple_plural(len(new_articles), 'article'), site), progress))
			except Exception as error:
				logerr('Fail')
				logerr(str(error))
		else:
			module = d["module"]
			kwargs = d["kwargs"]
			
			try:
				found = module.get_articles(**kwargs)
				for i in found:
					articles.put(i)
				update_progress(progress,
					100.0 / (len(config.sites_to_parse) + len(config.rss_feeds)) / 2.0)
				log(show_progress(s.format(len(found),
					simple_plural(len(found), 'article'), site), progress))
			except Exception as error:
				logerr("Failed to parse articles from {0}".format(site))
				logerr(str(error))

def update_progress(shared_object, num):
	shared_object.value += num

def dump_articles(filename="articles_dumped"):
	"""Dump articles to ~/.tech-parser/<filename>"""
	
	m = multiprocessing.Manager()
	
	articles = m.Queue()
	
	progress = m.Value('d', 0.0, lock=False)
	
	main_queue = m.Queue()
	
	for i in get_conf.config.sites_to_parse:
		main_queue.put(i)

	for i in get_conf.config.rss_feeds:
		main_queue.put(i)
	
	pool = multiprocessing.Pool(processes=get_conf.config.num_threads)
	
	for i in range(get_conf.config.num_threads):
		pool.apply_async(parse_site, (main_queue, articles, progress))
	
	pool.close()
	pool.join()
	
	articles_before = [i[0] for i in load_articles()]
	list_articles = []
	while not articles.empty():
		list_articles.append(articles.get())
	
	log("Total articles: %d" %(len(list_articles)))
	log("New articles: %d"
		%(len([i for i in list_articles if i not in articles_before])))
	
	if get_conf.config.save_articles:
		log("Saving articles to archive...")
		
		setup_db()
		con = sqlite3.connect(os.path.join(logdir, "archive.db"))
		cur = con.cursor()
		
		for article in list_articles:
			title = article["title"]
			link = article["link"]
			source = article["source"]
			
			try:
				cur.execute("""INSERT INTO articles(title, link, source)
					values(?, ?, ?);""", (title, link, source))
			except sqlite3.IntegrityError:
				pass
		
		con.commit()
		con.close()
	
	num = len(recommend.get_interesting_articles(db=get_conf.config.db))
	num += len(recommend.get_blacklist(db=get_conf.config.db))
	
	if num >= 20:
		log("Ranking articles...")
		list_articles = recommend.find_similiar(list_articles, db=get_conf.config.db)
		list_articles.sort(key=lambda x: x[1], reverse=True)
	else:
		log("Shuffling articles...")
		shuffle(list_articles)
		list_articles = [[a, -1] for a in list_articles]
	
	log("Dumping data to file: {0}...".format(filename))
	
	dumped = pickle.dumps(list_articles)
	path = os.path.join(os.path.expanduser("~"), ".tech-parser")
	path = os.path.join(path, filename)
	f = open(path, "wb")
	f.write(dumped)
	f.close()
	
	log("Done!")

def dump_articles_per(s):
	"""Dump articles per <s> seconds"""
	
	while True:
		if int(time()) % s == 0:
			dump_articles()
		sleep(1)

def filter_articles(articles):
	"""Filter articles"""
	
	config = get_conf.config
	
	articles_filtered = []
	
	for article in articles:
		passing = True
		
		words_len = len(config.filters["All"]["or"])
		title = article[0]["title"].lower()
		
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
			articles_filtered.append(article)
	
	return articles_filtered

def load_articles(filename="articles_dumped"):
	"""Load articles from ~/.tech-parser/<filename>"""
	
	log("Reading articles from file: {0}...".format(filename))
	try:
		f = open(os.path.join(logdir, filename), 'rb')
	except IOError:
		log("File '{0}' doesn't exist: returning empty list".format(filename))
		return []
	
	dumped = f.read()
	f.close()
	
	articles = pickle.loads(dumped)
	
	log("Done!")
	
	return articles

@route('/static/<filename:path>')
def serve_static(filename):
	"""Serve static files"""
	
	return static_file(filename, root=static_dir_path)

def update_liked_disliked():
	global liked, disliked, liked_links, disliked_links

	config = get_conf.config
	
	liked = recommend.get_interesting_articles(db=config.db)
	disliked = recommend.get_blacklist(db=config.db)
	liked_links = [i['link'] for i in liked]
	disliked_links = [i['link'] for i in disliked]

@route('/histadd/<addr:path>')
def add_to_history(addr):
	
	recommend.add_article(addr, db=get_conf.config.db)
	
	update_liked_disliked()
	
@route('/blacklistadd/<addr:path>')
def add_to_blacklist(addr):
	recommend.add_article_to_blacklist(addr, db=get_conf.config.db)
	
	update_liked_disliked()

@route('/blacklistrm/<addr:path>')
def rm_from_blacklist(addr):
	recommend.remove_from_blacklist(addr, db=get_conf.config.db)
	
	update_liked_disliked()

@route('/histrm/<addr:path>')
def rm_from_history(addr):
	recommend.remove_from_history(addr, db=get_conf.config.db)
	
	update_liked_disliked()

@route('/history')
@route('/history/<page_number>')
def show_history(page_number=1):
	history_page = mylookup.get_template('history.html')
	q = unicode_(request.GET.get('q', ''))
	
	articles = recommend.get_interesting_articles(db=get_conf.config.db)
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	if q:
		qs = q.lower().split()
		articles = filter(lambda x: has_words(qs, x), articles)
	
	articles = map(lambda x: replace_newlines(escape_link(x)), articles)
	
	all_articles = articles
	articles = split_into_pages(articles, 30)
	try:
		requested_page = articles[page_number-1]
	except IndexError:
		requested_page = []
	
	return history_page.render(articles=requested_page,
		num_pages=len(articles),
		page_num=page_number,
		q=q,
		all_articles=all_articles)

@route('/blacklist')
@route('/blacklist/<page_number>')
def show_blacklist(page_number=1):
	history_page = mylookup.get_template('blacklist.html')
	q = unicode_(request.GET.get('q', ''))
	
	articles = recommend.get_blacklist(db=get_conf.config.db)
	
	try:
		page_number = int(page_number)
	except ValueError:
		page_number = 1
	
	if q:
		qs = q.lower().split()
		articles = filter(lambda x: has_words(qs, x), articles)
	
	articles = map(lambda x: replace_newlines(escape_link(x)), articles)
	
	all_articles = articles
	articles = split_into_pages(articles, 30)
	try:
		requested_page = articles[page_number-1]
	except IndexError:
		requested_page = []
	
	return history_page.render(articles=requested_page,
		num_pages=len(articles),
		page_num=page_number,
		q=q,
		all_articles=all_articles)

def has_words(qs, article):
	"""Check if article contains words"""
	
	title = unicode_(article['title']).lower()
	summary = unicode_(article['summary']).lower()
	
	for i in qs:
		if i not in title and i not in summary:
			return False
	return True

def escape_link(article):
	"""Escape HTML tags, etc."""
	
	new_article = {}
	new_article.update(article)
	new_article['original_link'] = new_article['link']
	
	new_article['link'] = urlencode(encoded_dict({'': new_article['link']}))[1:]
	return new_article

def set_liked(articles):
	for article in articles:
		article['liked'] = article['original_link'] in liked_links
		article['disliked'] = article['original_link'] in disliked_links

def replace_newlines(article):
	new_article = {}
	new_article.update(article)
	new_article['summary'] = new_article['summary'].replace('\n', '<br/>')
	
	return new_article

@route("/")
@route("/<page_number>")
def article_list(page_number=1):
	"""Show list of articles | Search for articles"""
	
	main_page = mylookup.get_template("articles.html")
	q = unicode_(request.GET.get('q', ''))
	
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
		articles = filter(lambda x: has_words(qs, x[0]), articles)
	
	articles = map(lambda x: replace_newlines(escape_link(x[0])), articles)
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
		q=q,
		all_articles=all_articles,)

class ParserDaemon(Daemon):
	def __init__(self):
		pidfile = os.path.join(logdir, "tech-parser.pid")
		so = open(os.path.join(logdir, "output.log"), "a+")
		se = open(os.path.join(logdir, "error.log"), "a+")
		if os.stat(so.name).st_size > 102400:
			so.truncate()
		if os.stat(se.name).st_size > 102400:
			se.truncate()
		
		super(ParserDaemon, self).__init__(pidfile, stdout=so, stderr=se)
	
	def onStart(self):
		run_server(host=get_conf.config.host, port=get_conf.config.port)

def is_hostname(hostname):
	if len(hostname) > 255:
		return False
	if hostname[-1] == ".":
		hostname = hostname[:-1]
	allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
	return all(allowed.match(x) for x in hostname.split("."))

def run_server(host, port):
	config = get_conf.config
	
	p1 = multiprocessing.Process(target=dump_articles_per,
		args=(config.update_interval,))
	atexit.register(p1.terminate)
	p1.start()
	run(host=host, port=port, server=config.server)

if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(description="""\
Article parser.
Available commands: start|stop|restart|update|run HOST:PORT""")
	
	arg_parser.add_argument("action", nargs="+",
		action="store", default=[], help="Action to run")
	arg_parser.add_argument("--config", help="Path to configuration")
	arg_parser.add_argument("--num-threads",
		help="Number of threads for parsing articles")
	arg_parser.add_argument("--update-interval", help="Update interval")
	arg_parser.add_argument("--server", help="Server to use")
	arg_parser.add_argument("--db", choices=['sqlite', 'postgresql'],
		default='sqlite', help="Database to use: sqlite or postgresql")
	
	args = arg_parser.parse_args()
	
	if args.config:
		get_conf.set_config_from_fname(args.config)
	
	if args.num_threads:
		try:
			get_conf.config.num_threads = int(args.num_threads)
		except ValueError:
			logerr("'{0}' is not an integer".format(args.num_threads))
			sys.exit(1)

	if args.update_interval:
		try:
			get_conf.config.update_interval = int(args.update_interval)
		except ValueError:
			logerr("'{0}' is not an integer".format(args.update_interval))
			sys.exit(1)
	
	if args.server:
		get_conf.config.server = args.server
	
	get_conf.config.db = args.db
	
	if args.action:
		if args.action[0] == "run":
			if len(args.action) == 1:
				addr = get_conf.config.host + ":" + get_conf.config.port
			else:
				addr = args.action[1]
			if not ":" in addr:
				addr += ":80"
			elif addr.endswith(":"):
				addr += "80"
		
			host, port = addr.split(":")
			is_host_correct = is_hostname(host)
			
			try:
				is_port_correct = int(port) <= 65535 and int(port) > 0
			except ValueError:
				is_port_correct = False
				
			if not is_host_correct:
				logerr("Invalid hostname")
				sys.exit(1)
			elif not is_port_correct:
				logerr("Invalid port")
				sys.exit(1)
			else:
				run_server(host, port)
		elif args.action[0] == "update":
			dump_articles()
		elif args.action[0] == "start":
			running_as_daemon = True
			parser_daemon = ParserDaemon()
			try:
				parser_daemon.start()
			except DaemonError as e:
				logerr('Failed to start server: {0}'.format(e))
				sys.exit(1)
		elif args.action[0] == "stop":
			running_as_daemon = True
			parser_daemon = ParserDaemon()
			try:
				parser_daemon.stop()
			except DaemonError as e:
				logerr('Failed to stop server: {0}'.format(e))
				sys.exit(1)
else:
	app = default_app()
