
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

$(document).ready(function() {

$('.profile-view-tab-choice').each( function(index){
    $(this).click( function(index){
    object = $(this).attr('target');
    console.log('#'+object);
    $('.profile-view-tab-choice').attr('class', 'profile-view-tab-choice profile-view-tab-choice-off');
    $(this).attr('class', 'profile-view-tab-choice profile-view-tab-choice-on');
    $('#profile-view-bookmark>div').css("display", "none");
    $('#'+object).css('display','block');
});
});

$('.notification-row').each(function(){

    $(this).click(function(){
        pk = $(this).attr('notification-pk');
        console.log(pk);
    $.post('/accounts/ajax/read-notification/', {pk:pk}, function(response){
    console.log(response);},'json' );
    $(this).attr("class", "notification-row notification-read");
    });
    });

});


