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


$(window).on('load resize',  function () {
    $('.nav-sidebar').toggleClass('nav-pills', $(window).width() < 768);
});

$(document).ready(function() {


// this could enable tooltip on generated elements 
$('body').tooltip({ selector:'[data-toggle=tooltip]'});
$(".alert").alert()

$("#id_tags").select2();
$("#s2id_id_tags").css("padding","0px").css("border", "0px");
// neeed to change the css of the respective file to change the tag select style.
//$(".select2-search-choice").css("margin-top","5px").css("background-color","#e0eaf1");
//$(".select2-search-choice").css("color","#4a6b82").css("background-image","None");
//

$(".jRating").jRating(
  {
  bigStarsPath: '/static/lib/jRating/icons/stars.png',
  smallStarsPath: '/static/lib/jRating/icons/small.png',
  isDisabled: true,
  rateMax: 10,
  type:'small',
  sendRequest: false,
});

});
