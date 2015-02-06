function toggleText(element) {
	var $article = $(element).parent('h3').parent('.article');
	var $summary = $article.find('.summary');
	if ($summary.css('display') != 'block') {
		$summary.fadeIn('fast');
		$summary.find('img').each(function() {
			$(this).attr('src', $(this).attr('data-src'));
		});
	} else {
		$summary.fadeOut('fast');
	}
}

function add_to(where, $element) {
	var $summary = $element.parent('.summary');
	var $article = $summary.parent('.article');
	var link = $article.attr('data-escaped-link');
	
	if (where == 'history') {
		$.get('/histadd/' + link, function(data) {
			$element.attr('class', 'like liked');
		});
	} else if (where == 'blacklist') {
		$.get('/blacklistadd/' + link, function(data) {
			$element.attr('class', 'dislike disliked');
		});
	}
}

function RateArticle(element) {
	var $element = $(element);
	if ($element.hasClass('like'))
		if ($element.hasClass('liked')) {
			remove_from('history', $element);
		} else {
			add_to('history', $element);
	} else if ($element.hasClass('dislike')) {
		if ($element.hasClass('disliked')) {
			remove_from('blacklist', $element);
		} else {
			add_to('blacklist', $element);
		}
	}
}

function remove_from(where, $element) {
	var $summary = $element.parent('.summary');
	var $article = $summary.parent('.article');
	var link = $article.attr('data-escaped-link');
	
	if (where == 'history') {
		var url = '/histrm/' + link;
		$.get(url, function(data) {
			$element.attr('class', 'like');
		});
	} else if (where == 'blacklist') {
		var url = '/blacklistrm/' + link;
		$.get(url, function(data) {
			$element.attr('class', 'dislike');
		});
	}
}

function onLoad() {
	$(document).ready(function() {
		var valueBefore = $('#searchbox input').css('width');
		$('#searchbox input').focusin(function() {
			var maxValue = parseInt($('#searchbox input').css('max-width'));
			var searchBox = $('#searchbox');
			var searchBoxWidth = parseInt(searchBox.css('width'))
			searchBoxWidth += parseInt(searchBox.parent().css('margin-left'));
			searchBoxWidth += parseInt(searchBox.parent().css('margin-right'));
			var btn = $('#searchbox button');
			var btnWidth = parseInt(btn.css('width'));
			btnWidth += parseInt(btn.css('margin-left'));
			btnWidth += parseInt(btn.css('margin-right'));
			btnWidth += parseInt(btn.css('padding-left'));
			btnWidth += parseInt(btn.css('padding-right'));
			if (maxValue + btnWidth >= searchBoxWidth) {
				$('#searchbox button').fadeOut('fast');
				setTimeout(function() {
					$('#searchbox input').animate({width: maxValue + 'px'}, 400);
				}, 80);
			} else {
				$(this).animate({width: maxValue + 'px'}, 400);
			}
		})
		$('#searchbox input').focusout(function() {
			$(this).animate({width: valueBefore}, 400);
			setTimeout(function() {$('#searchbox button').fadeIn('fast')}, 400);
		});
		
		$('.triangle-spoiler').click(function() {
			var $this = $(this);
			var $element = $this.parent().find('.triangle-spoiler-data');
			
			if ($element.css('display') == 'none') {
				$element.fadeIn('fast');
				$this.attr('data-opened', 'true');
			} else {
				$element.fadeOut('fast');
				$this.attr('data-opened', 'false');
			}
		});
		
		$('.delete-icon').click(function() {
			var $this = $(this);
			if ($this.hasClass('delete-icon')) {
				$this.parent().find('.triangle-spoiler').css('text-decoration', 'line-through');
				$this.attr('class', 'undo-icon');
				$this.parent().find('input[data-field-name=is_deleted]').val('1');
			} else if ($this.hasClass('undo-icon')) {
				$this.parent().find('.triangle-spoiler').css('text-decoration', 'inherit');
				$this.attr('class', 'delete-icon');
				$this.parent().find('input[data-field-name=is_deleted]').val('0');
			}
		});
		
		var swipefunc = function(e, d, distance) {
			if (distance < 150) {
				return;
			}
			var curHref = window.location.href;
			var vars = curHref.match(/\?.+/);
			curHref = curHref.replace(/\?.*/g, '');
			
			var pgnum = curHref.match(/\d+$/);
			if (pgnum === null) {
				pgnum = "1";
			} else {
				curHref = curHref.slice(0, curHref.length-(pgnum.length+1));
			}
			if (d == 'left')
				var newPgnum = parseInt(pgnum) + 1;
			else
				var newPgnum = parseInt(pgnum) - 1;
			
			var newUrl = curHref;
			if (curHref[curHref.length-1] != '/') {
				newUrl += '/';
			}
			newUrl += newPgnum;
			if (vars !== null) {
				newUrl += vars;
			}
			window.location.href = newUrl;
		};
		
		$('#main').swipe({swipeLeft: swipefunc, swipeRight: swipefunc,
			treshold: 0});
		
		var $imgs = $('.article .summary img');
		$imgs.each(function() {
			$(this).attr('data-src', $(this).attr('src'));
			$(this).removeAttr('src');
		});
	});
}

function parsingTime(interval) {
	var remains = Math.floor((interval - (new Date().getTime() / 1000) % interval) / 60);
	return remains + simplePlural(' minute', remains)
}

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function simplePlural(str, n) {
	var str_n = '' + n;
	if (!endsWith(str_n, '1') || str_n == '11') {
		str += 's';
	}
	return str;
}

function AddFeed() {
	$new_feed = $('#new-feed');
	$new_feed.css('display', 'inherit');
	$new_feed.find('input[name=new_feed]').val('0');
}
