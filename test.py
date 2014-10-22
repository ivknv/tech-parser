#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import (smashingmagazine, digg, habrahabr, gizmodo, techcrunch, verge,
venturebeat, zdnet, helpix, mobilereview, trashbox, readwrite, droider,
redroid, hackernews, dzone, topdesignmag, reddit, medium, androidcentral,
codeproject, engadget, flowa, ittoolbox, ixbt, maketecheasier, mashable,
techrepublic, planetclojure, recode, slashdot, threednews, wired, geektimes)

parsers = [smashingmagazine, digg, habrahabr, gizmodo, techcrunch, verge,
	venturebeat, zdnet, helpix, mobilereview, trashbox, readwrite, droider,
	redroid, hackernews, dzone, topdesignmag, reddit, medium, androidcentral,
	codeproject, engadget, flowa, ittoolbox, ixbt, maketecheasier, mashable,
	techrepublic, planetclojure, recode, slashdot, threednews, wired, geektimes]

def test(parsers=[[p, [], dict()] for p in parsers]):
	total_correct, total_incorrect = 0.0, 0.0
	
	for parser in parsers:
		args = ', '.join(list(map(lambda x: repr(str(x)), parser[1])) + \
			['{}={}'.format(kwarg, repr(parser[2][kwarg]))
				for kwarg in parser[2]])
		print('Testing {}.get_articles({})'.format(parser[0].__name__, args))
		result = parser[0].get_articles(*parser[1], **parser[2])
		print('Total articles: {}'.format(len(result)))
		correct, incorrect = 0.0, 0.0
		required_fields = ['title', 'link', 'summary', 'source']
		for article in result:
			missing_fields = []
			for field in required_fields:
				if field not in article:
					incorrect_fields.append(field)
					print("Missing '{}' field".format(field))
			
			if missing_fields:
				incorrect += 1
			else:
				correct += 1
		
		try:
			percent = correct / (correct + incorrect) * 100.0
		except ZeroDivisionError:
			percent = 0.0
		
		print('{}% of articles are formated correcly'.format(percent))
		total_correct += correct
		total_incorrect += incorrect
	
	try:
		return total_correct / (total_correct + total_incorrect)
	except ZeroDivisionError:
		return 0.0

if __name__ == '__main__':
	print(test())
