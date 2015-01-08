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

function ignore_article(element) {
	var $summary = $(element).parent('.summary');
	var $article = $summary.parent('.article');
	var link = $article.attr('data-escaped-link');
	$.get('/blacklistadd/' + link, function(data) {
		$article.fadeOut();
	});
}

function add_to_history(element) {
	var $summary = $(element).parent('.summary');
	var $article = $summary.parent('.article');
	var link = $article.attr('data-escaped-link');
	$.get('/histadd/' + link, function(data){});
}

function remove_from(where, element) {
	var $summary = $(element).parent('.summary');
	var $article = $summary.parent('.article');
	var link = $article.attr('data-escaped-link');
	
	if (where == 'history' || where == 'blacklist') {
		if (where == 'history') {
			var url = '/histrm/' + link;
		} else if (where == 'blacklist') {
			var url = '/blacklistrm/' + link;
		}
		$.get(url, function(data) {
			$article.fadeOut();
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
		
		swipefunc = function(e, d, distance) {
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

function login(return_path) {
	var $input = $('input[name=password]');
	$.post('/checkpass/', {password: $input.val()},
		function(data) {
			if(data.success) {
				window.location.href = return_path;
			} else {
				alert('Invalid password');
			}
	}, 'json');
}
