
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
/* add an edit button to each section title */


$(document).ready(function() {
    var wiki_title = $('#wiki-content h1').html();
    
    console.log(wiki_title);
    $('#wiki-content h2,h3,h4,h5,h6').each( function(){
        var header = $(this).get(0).tagName;
        var section_name = $(this).html();
        var href_html = '/wiki/'+wiki_title+'/edit-section/?'+'header='+header+'&name='+section_name;
        $(this).html( $(this).html()+" <small>[<a href='"+ href_html + "'>edit</a>]</small>");
        });
        
/*        
    $('#wiki-content h2,h3,h4,h5,h6').each( function(){
        var header = $(this).get(0).tagName;
    $(this).children().children().click(function(){
        var section_name = $(this).attr('section');
        
        console.log(header+section_name);
        $.get('/wiki/'+wiki_title+'/edit-section/?section='+section_name, {title:wiki_title, header:header,name:section_name}, function(response){
        console.log(response);
    }, "json");

        //alert("hello");
    });
    });
*/    
});
