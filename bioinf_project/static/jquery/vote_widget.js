
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
    } else if (response.yourvote == 0){
        vote_up.attr('class', 'vote-up-off');
        vote_down.attr('class', 'vote-down-off');

    } else if (response.yourvote == -1){
        vote_up.attr('class', 'vote-up-off');
        vote_down.attr('class', 'vote-down-on');

    }
        elem.children('div.vote-count-obj').text(response.allvote)
        console.log(vote_up.attr('class'));
        console.log(vote_down.attr('class'));

}

$(document).ready(function() {
    $('div.vote-widget a').each( function(index){
        
    $(this).click( function(index){
    var content_type = $(this).parent().attr('data-obj-name');
    var id = $(this).parent().attr('data-obj-id');
    var vote_status = $(this).attr('class');
    console.log( index + content_type +',' + id + ',' + vote_status );
    elem = $(this).parent();

    $.post('/ajax/vote/', {ct:content_type, id:id, vstat:vote_status}, function(response){
    toggle_vote_widget(elem, response);
    }, "json");


});
});
});
