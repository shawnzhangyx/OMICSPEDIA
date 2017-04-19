
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/* toggle the vote options */
function toggle_vote_widget(elem, response){
    console.log(response.yourvote);
    // elem = $('div.vote-widget')
    var vote_up = elem.children().first(); // this selector needs to be modified.
    var vote_down = elem.children().last(); // testing purpose only.

    if (response.yourvote == 1){
        vote_up.attr('class', 'vote-up-on');
        vote_down.attr('class', 'vote-down-off');
        vote_up.attr('title', "you've already voted.");
        vote_down.attr('title', "you've already voted.");
    } else if (response.yourvote == 0){
        alert(response.message);

    } else if (response.yourvote == -1){
        vote_up.attr('class', 'vote-up-off');
        vote_down.attr('class', 'vote-down-on');
        vote_up.attr('title', "you've already voted.");
        vote_down.attr('title', "you've already voted.");
    }
        elem.children('div.vote-count-obj').text(response.allvote)
        console.log(vote_up.attr('class'));
        console.log(vote_down.attr('class'));

}

function toggle_vote_up_widget(elem, response){
    console.log(response.yourvote);
    var vote_up = elem.children().first(); // this selector needs to be modified.

    if (response.yourvote == 1){
        vote_up.attr('class', 'vote-up-sm-on');
    } else if (response.yourvote == 0){
        alert(response.message);
    }
        elem.children('div.vote-count-sm-obj').text(response.allvote)
        console.log(vote_up.attr('class'));

}


function toggle_bookmark_widget(elem, response){
    console.log(response.yourvote);
    var bookmark = elem.children().first(); // this selector needs to be modified.

    if (bookmark.hasClass('bookmark-off')){
        bookmark.attr('class', 'bookmark-on');
        bookmark.attr('title', 'double click to cancel bookmark');
    } else {
        bookmark.attr('class', 'bookmark-off');
        bookmark.attr('title', 'double click to add bookmark');

    }
        elem.children('div.bookmark-count').text(response.bookmark_count)
        console.log(bookmark.attr('class'));

}

$(document).ready(function() {
    $('div.vote-widget>.vote-open').each( function(index){

    $(this).dblclick( function(index){
    var content_type = $(this).parent().attr('data-obj-name');
    var id = $(this).parent().attr('data-obj-id');
    var vote_status = $(this).attr('class');
    console.log( index + content_type +',' + id + ',' + vote_status );
    elem = $(this).parent();

    $.post('/ajax/vote/', {ct:content_type, id:id, vstat:vote_status}, function(response){
    toggle_vote_widget(elem, response);
    console.log(id);
    }, "json");
});
});

$('div.vote-up-widget>.vote-open').each( function(index){
    $(this).dblclick( function(index){
    var content_type = $(this).parent().attr('data-obj-name');
    var id = $(this).parent().attr('data-obj-id');
    var vote_status = $(this).attr('class');
    console.log( index + content_type +',' + id + ',' + vote_status );
    elem = $(this).parent();

    $.post('/ajax/vote/', {ct:content_type, id:id, vstat:vote_status}, function(response){
    toggle_vote_up_widget(elem, response);
    }, "json");
});
});

$('div.bookmark-widget a').each( function(index){
    $(this).dblclick( function(index){
    var content_type = $(this).parent().attr('data-obj-name');
    var id = $(this).parent().attr('data-obj-id');
    var bookmark_status = $(this).attr('class');
    console.log( index + content_type +',' + id + ',' + bookmark_status );
    elem = $(this).parent();

    $.post('/ajax/bookmark/', {ct:content_type, id:id, bstat:bookmark_status}, function(response){
    toggle_bookmark_widget(elem, response);
    }, "json");
});
});

});
