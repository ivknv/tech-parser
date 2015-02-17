/**
 * Check if string starts with other string
 * @param {String} str Other string
 * @returns {Boolean}
 */
String.prototype.startsWith = function(str) {
    return this.indexOf(str) === 0;
}

/**
 * Toggle article spoiler with text
 * @param {Element} element Spoiler element
 */
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

/**
 * Adds article to history or blacklist depending on arguments via AJAX request
 * @param {String} where Can be 'history' or 'blacklist'. Is a destination the article needs to be added to
 * @param {jQuery} $element Article element
 */
function add_to(where, $element) {
	var $summary = $element.parent('.summary');
	var $article = $summary.parent('.article');
	var link = $article.attr('data-escaped-link');
	
	if (where == 'history') {
        /* Add article to history and mark it as liked */
		$.get('/histadd/' + link, function(data) {
			$element.attr('class', 'like liked');
		});
	} else if (where == 'blacklist') {
        /* Add article to blacklist and mark it as disliked */
		$.get('/blacklistadd/' + link, function(data) {
			$element.attr('class', 'dislike disliked');
		});
	}
}

/**
 * Rates article (like or dislike) via AJAX request
 * @param {Element} element Like or dislike button
 */
function RateArticle(element) {
	var $element = $(element);
    
	if ($element.hasClass('like'))
        /* Remove article from history if it's already there */
		if ($element.hasClass('liked')) {
			remove_from('history', $element);
		} else {
			add_to('history', $element);
	} else if ($element.hasClass('dislike')) {
        /* Remove article from blacklist if it's already there */
		if ($element.hasClass('disliked')) {
			remove_from('blacklist', $element);
		} else {
			add_to('blacklist', $element);
		}
	}
}

/**
 * Removes article from history or blacklist depending on arguments via AJAX request
 * @param {String} where Can be 'history' or 'blacklist'. Is a destination the article needs to be removed from
 * @param {jQuery} $element Article element
 */
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

/**
 * Opens spoiler
 * @param {jQuery} $element Element that is going to be shown
 * @param {jQuery} $spoiler Spoiler element
 */
function OpenSpoiler($element, $spoiler) {
    $element.fadeIn('fast');
    $spoiler.attr('data-opened', 'true');
}

/**
 * Closes spoiler
 * @param {jQuery} $element Element that is going to be hidden
 * @param {jQuery} $spoiler Spoiler element
 */
function CloseSpoiler($element, $spoiler) {
    $element.fadeOut('fast');
    $spoiler.attr('data-opened', 'false');
}

/**
 * Opens/closes spoiler
 * @param {jQuery} $element Element that is going to be hidden/shown
 * @param {jQuery} $spoiler Spoiler element
 */
function ToggleSpoiler($element, $spoiler) {
    if ($element.css('display') == 'none') {
        OpenSpoiler($element, $spoiler);
    } else {
        CloseSpoiler($element, $spoiler);
    }
}

/**
 * Wrapper for ToggleSpoiler function. This function is basically a handler for click event
 */
function ToggleSpoilerWrapper() {
    var $this = $(this);
    var $element = $this.parent().find('.triangle-spoiler-data');
    return ToggleSpoiler($element, $this);
}

/**
 * Marks feed as not deleted
 * @param {jQuery} $element
 */
function UndoDeleteFeed($element) {
    var $element_parent = $element.parent();
    $element_parent.find('.triangle-spoiler').css('text-decoration', 'inherit');
    $element.attr('class', 'delete-icon');
    
    /* Actually mark feed */
    $element_parent.find('input[data-field-name=is_deleted]').val('0');
}

/**
 * Marks feed as deleted
 * @param {JQuery} $element 
 */
function DeleteFeed($element) {
    var $element_parent = $element.parent();
    $element_parent.find('.triangle-spoiler').css('text-decoration', 'line-through');
    $element.attr('class', 'undo-icon');
    
    /* Actually mark feed */
    $element_parent.find('input[data-field-name=is_deleted]').val('1');
}

/**
 * Determines what is this icon and if it's a delete icon then it marks feed as deleted,
 * if it's undo icon then it marks feed as not deleted
 */
function SpoilerIconOnClick() {
    var $this = $(this);
    if ($this.hasClass('delete-icon')) {
        DeleteFeed($this);
    } else if ($this.hasClass('undo-icon')) {
        UndoDeleteFeed($this);
    }
}

/**
 * Does things that should be done after loading page such as adding handlers for various elements
 */
function onLoad() {
	$(document).ready(function() {
        /* This part of code a bit complicated
           It tries to properly extend search field and remove search button if necessary */
		var valueBefore = $('#searchbox input').css('width');
		$('#searchbox input').focusin(function() {
			var maxValue = parseInt($('#searchbox input').css('max-width'));
			var searchBox = $('#searchbox');
			var searchBoxWidth = parseInt(searchBox.css('width'))
            var searchBox_parent = searchBox.parent();
            var btn = $('#searchbox button');
            var btnWidth = parseInt(btn.css('width'));
            
            /* Calculating widths */
			searchBoxWidth += parseInt(searchBox_parent.css('margin-left'));
			searchBoxWidth += parseInt(searchBox_parent.css('margin-right'));
            
			btnWidth += parseInt(btn.css('margin-left'));
			btnWidth += parseInt(btn.css('margin-right'));
			btnWidth += parseInt(btn.css('padding-left'));
			btnWidth += parseInt(btn.css('padding-right'));
            
            /* Remove button and delay search field animation if necessary */
			if (maxValue + btnWidth >= searchBoxWidth) {
				$('#searchbox button').fadeOut('fast');
				setTimeout(function() {
					$('#searchbox input').animate({width: maxValue + 'px'}, 400);
				}, 80);
			} else {
				$(this).animate({width: maxValue + 'px'}, 400);
			}
		});
        
        /* Some callbacks */
		$('#searchbox input').focusout(function() {
			$(this).animate({width: valueBefore}, 400);
			setTimeout(function() {$('#searchbox button').fadeIn('fast')}, 400);
		});
		
		$('.triangle-spoiler').click(ToggleSpoilerWrapper);
		
		$('.delete-icon').click(SpoilerIconOnClick);
		
        /* Swipe gestures to change page */
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

/**
 * Show new feed
 */
function AddFeed() {
	var $new_feed = $('#new-feed');
	$new_feed.css('display', '');
    /* Enable new feed. This might be confusing but '1' means disabled and '0' means enabled
       It's basically is_deleted field. */
	$new_feed.find('input[name=new_feed]').val('0');
    OpenSpoiler($new_feed.find('.triangle-spoiler-data'), $new_feed.find('.triangle-spoiler'));
}

/**
 * Hide new feed that appears after clicking 'Add new feed' button
 */
function HideNewFeed() {
    var $new_feed = $('#new-feed');
    $new_feed.css('display', 'none');
    
    /* Disable new feed. This might be confusing but '1' means disabled and '0' means enabled
       It's basically is_deleted field. */
    $new_feed.find('input[name=new_feed]').val('1');
    CloseSpoiler($new_feed.find('.triangle-spoiler-data'), $new_feed.find('.triangle-spoiler'))
}

/**
 * Show errors at the place where they were found
 * @param {Object} errors List of errors
 */
function ShowErrors(errors) {
    for (var key in errors) {
        if (errors.hasOwnProperty(key)) {
            /* Prepend error block */
            var $element = $('[data-name=' + key + ']').prepend('<div class="error-block"></div>');
            
            /* Find it */
            var $error_block = $element.find('.error-block');
            
            /* Add error messages to it */
            $.each(errors[key], function(i,v) {
                $error_block.append("<div class='error'></div>");
                $error_block.find('.error:last-child').html(v);
            });
        }
    }
}

/**
 * Adds another RSS feed to list. It just basically adds HTML code.
 * @param {Object} rss_feed RSS feed object that contains its properties
 * @param {String|Number} rss_feed.hash RSS feed hash
 * @param {String} rss_feed.name RSS feed name
 * @param {String} rss_feed['short-name'] RSS feed short name
 * @param {String} rss_feed.url RSS feed URL
 * @param {String} rss_feed.icon RSS feed icon URL
 * @param {Boolean} rss_feed.enabled Allows to determine if RSS feed is enabled or not
 */
function AppendRSSFeed(rss_feed) {
    var $form = $('#rss_feeds_form');
    $form.find('.rss-feed').last().after(
        '<div class="rss-feed margin-bottom">' +
            '<input type="hidden" name="is_deleted_' + rss_feed.hash + '" value="0" data-field-name="is_deleted" autocomplete="off" />' +
            '<div class="triangle-spoiler" data-opened="false">' + rss_feed.name + '</div>\n' + 
            '<div class="delete-icon"></div>' +
            '<div class="triangle-spoiler-data" data-name="rss_feed_' + rss_feed.hash + '">' +
                '<div class="margin-bottom">' +
                    '<input type="checkbox" name="enabled_' + rss_feed.hash + '" value="1" autocomplete="off" />' +
                    '<label for="enabled_' + rss_feed.hash + '">Enabled</label>' +
                '</div>' +
                '<div class="margin-bottom">' +
                    '<label for="name_' + rss_feed.hash + '">Feed name:</label>' +
                    '<input class="input" type="text" value="' + rss_feed.name + '" ' +
                        'name="name_' + rss_feed.hash +'" autocomplete="off" placeholder="Feed name" />' +
                '</div>' +
                '<div class="margin-bottom">' +
                    '<label for="sn_' + rss_feed.hash + '">Feed short name:</label>' +
                    '<input class="input" type="text" value="' + rss_feed['short-name'] +
                        '" name="sn_' + rss_feed.hash + '" autocomplete="off" placeholder="feed-short-name" />' +
                '</div>' + 
                '<div class="margin-bottom">' +
                    '<label for="url_' + rss_feed.hash + '">Feed url:</label>' +
                    '<input class="input" type="url" value="' + rss_feed.url + '" ' +
                        'name="url_' + rss_feed.hash + '" autocomplete="off" ' + 
                        'placeholder="http://example.com/feed-url" />' +
                '</div>' +
                '<div class="margin-bottom">' +
                    '<label for="icon_' + rss_feed.hash + '">Feed icon url:</label>' +
                    '<input class="input" type="url" value="' + rss_feed.icon + '" ' + 
                        'name="icon_' + rss_feed.hash + '" autocomplete="off" ' +
                        'placholder="http://example.com/icon" />' +
                '</div>' +
                '<div class="margin-bottom">' +
                    '<label for="color_' + rss_feed.hash + '">Feed title color:</label>' +
                    '<input class="input" type="color" value="' + rss_feed.color + '" ' +
                        'name="color_' + rss_feed.hash + '" autocomplete="off" />' +
                '</div>' +
            '</div>' +
        '</div>');
    var $rss_feed = $form.find('.rss-feed').last();
    $rss_feed.find('.triangle-spoiler').click(ToggleSpoilerWrapper);
    $rss_feed.find('.delete-icon').click(SpoilerIconOnClick);
    $rss_feed.find('input[name=enabled_' + rss_feed.hash + ']').prop('checked', rss_feed.enabled);
}

/**
 * Clear and hide new feed that appears after clicking 'Add new feed' button
 */
function ClearNewFeed() {
    $('#new-feed input[name=new_feed_enabled]').val('1').prop('checked', true);
    $('#new-feed input[name=new_feed_name]').val('');
    $('#new-feed input[name=new_feed_sn]').val('');
    $('#new-feed input[name=new_feed_url]').val('');
    $('#new-feed input[name=new_feed_icon]').val('');
    $('#new-feed input[name=new_feed_color]').val('#000');
    HideNewFeed()
}

/**
 * Updates name and data-name attribute values by changing hash inside them
 * @param {String} old_hash Old hash
 * @param {String} new_hash New hash
 */
function UpdateHashes(old_hash, new_hash) {
    /* Update name attribute values */
    $('[name$=_' + old_hash + ']').each(function() {
        var $this = $(this);
        var old_name = $this.attr('name');
        $this.attr('name', old_name.slice(0, old_name.search('_' + old_hash)) + '_' + new_hash);
    });
    
    /* Update data-name attribute values */
    $('[data-name$=_' + old_hash + ']').each(function() {
        var $this = $(this);
        var old_data_name = $this.attr('data-name');
        $this.attr('data-name',
            old_data_name.slice(0, old_data_name.search('_' + old_hash)) + '_' + new_hash);
    });
}

/**
 * Updates field attributes and values. Used after sending AJAX request to update configuration.
 * @param {Array} modified Array of field names, data-names, hashes that were modified
 */
function UpdateFields(modified) {
    if (modified) {
        $.each(modified, function(i, v) {
            var name = v[0];
            var value = v[1];
            if (name.startsWith('hash_')) {
                /* Update field attributes */
                UpdateHashes(name.slice(5), value);
            } else {
                if (name.startsWith('name_')) {
                    /* Update spoilers */
                    $('[data-name$=_' + name.slice(5) + ']').parent().find('.triangle-spoiler').html(value);
                } else if (name.startsWith('enabled_')) {
                    $('input[name=' + name + ']').prop('checked', value);
                }
                $('input[name=' + name + ']').val(value);
            }
        });
    }
}

/**
 * Submits form via AJAX request
 * @param {String} type Type of form
 */
function AJAXSubmitForm(type) {
    /* Find corresponding form */
    var $form = $('#' + type + '_form');
    
    /* Clear all the error messages */
    $form.find('.error-block').remove();
    
    /* Send AJAX request */
	$.post('/update/', $form.serialize(), function(data) {
        /* Update fields and they attributes that were changed (including hashes) */
        UpdateFields(data['modified']);
        
        if (data['new_feed']) {
            /* Clear new feed */
            ClearNewFeed();
            
            var new_feed = data['new_feed'];
            
            /* Display new feed as regular (add it to list with others) */
            AppendRSSFeed({name: new_feed['name'],
                           'short-name': new_feed['short-name'],
                           url: new_feed['url'],
                           icon: new_feed['icon'],
                           color: new_feed['color'],
                           hash: new_feed['hash']});
        }
        
        if (data['deleted']) {
            /* Remove RSS feeds that were deleted on server */
            $.each(data['deleted'], function(i, v) {
                $form.find('[data-name=rss_feed_' + v[1] + ']').parent().remove();
            });
        }
        
        /* Show errors */
        ShowErrors(data.errors);
        
        $form.find('[data-name]').each(function() {
            var $this = $(this);
            
            /* Make text color green for a half second if there are no errors or
               make it red otherwise */
            if ($this.find('.error').length == 0) {
                if (type == 'parsers' || type == 'rss_feeds') {
                    var $spoiler = $this.parent().find('.triangle-spoiler');
                    $spoiler.css('color', 'green');
                    setTimeout(function() {
                        $spoiler.css('color', '');
                    }, 600);
                } else {
                    $this.css('color', 'green');
                    setTimeout(function() {
                        $this.css('color', '');
                    }, 600);
                }
            } else {
                var $data_name = $this.attr('data-name');
                if (type == 'parsers' || type == 'rss_feeds') {
                    var $spoiler = $this.parent().find('.triangle-spoiler');
                    $spoiler.css('color', 'red');
                    OpenSpoiler($this, $spoiler);
                } else {
                    $this.css('color', 'red');
                    setTimeout(function() {
                        $this.css('color', '');
                    }, 600);
                }
            }
        });
	}, 'json');
}
