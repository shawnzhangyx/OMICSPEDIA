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
    var wiki_title = $('#wiki-content h1').attr('title');

    // add an [edit] span to the end of each section. 
    $('#wiki-content h2,h3,h4,h5,h6').each( function(){
        var header = $(this).get(0).tagName;
        var section_name = $(this).html();
        var href_html = '/wiki/'+wiki_title+'/edit-section/?'+'header='+header+'&name='+section_name;
        $(this).html( $(this).html()+" <small>[<a href='"+ href_html + "'>edit</a>]</small>");
        });

    //differentiate functional wiki links and non-exist wiki links. 
    wikilinks=$('.wikilink')      
 //   console.log(wikilinks);
    arr = $.makeArray(wikilinks);
//    console.log(arr);
//    console.log($(arr).length);
    var titles = new Array;
    var i;
    for (i=0;i<$(arr).length;i++){
      titles.push( $(arr[i]).html() );
    }
 //   console.log(titles);
         $.get('/wiki/ajax/wikilinks/', {titles: titles}, function(data){
//        console.log(data.response);
        for(i=0;i<$(arr).length;i++){
          if (data.response[i]==0){
          $(arr[i]).removeClass('wikilink').addClass('wikilink-not-exist');
          $(arr[i]).attr('data-toggle','tooltip').attr('title', ' page does not exist').attr('data-placement','bottom');
          }
        }
    },'json');
    // add '[]' to the footnote items. 
    $('.footnote-ref').each(function(){
        $(this).html('['+$(this).html()+']');
    });
    // table of content 
    $('.toc').prepend("<p class='text-center'>Contents <a data-toggle='collapse' data-target='#toc-menu' href='#'>[hide]</a></p>");
    $('.toc ul').attr('id', 'toc-menu').attr('class', 'collapse in');
    $('#toc-menu').on('hide.bs.collapse', function() {
     $('.toc p a').html('[show]');
    })
     $('#toc-menu').on('show.bs.collapse', function() {
     $('.toc p a').html('[hide]');
    })
      // add rating function to the wiki article. 
      $("#jRating").jRating(
        {
        bigStarsPath: '/static/lib/jRating/icons/stars.png',
        smallStarsPath: '/static/lib/jRating/icons/small.png',
        rateMax: 10,
        canRateAgain: true,
        nbRates: 1,
        sendRequest: false,
        onClick: function(element, rate){
          console.log("haha");
          $('#jRating').attr('data-original-title',"your rating is recorded, thank you!");
        //  $('#jRating').tooltip('toggle');
          $('#jRating').tooltip('show');

                    $.post('/ajax/rate/', {title:wiki_title, rating:rate}, function(response){
          console.log(response);
    });

        }
      }
      );

    $('.userpage-collapse').click(function(){
       value = $(this).html();
       if (value == "expand"){
        $(this).next().css("display", "block");
        console.log($(this).next());
        $(this).html("collapse");
       }
       else {
        $(this).next().css("display", "none");
        $(this).html("expand");
        }
        });
      
});
