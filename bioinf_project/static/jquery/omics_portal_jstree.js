$(function() {
  $('#container').jstree({
  "core" : {
    "themes" : {
      "variant" : "normal"
    }
  },
    "plugins" : [ "search" ],
    "search": {
      "show_only_matches": false
    }
  });
  var to = false;
  $('#container-search').keyup(function () {
    if(to) { clearTimeout(to); }
    to = setTimeout(function () {
      var v = $('#container-search').val();
      $('#container').jstree(true).search(v);
    }, 250);
  });

  $('#omics-root').on('click', function () {
      $('#container').jstree(true).deselect_all();
      });

// monitering the status of the tree.
  $('#container').on('select_node.jstree', function (e, data) {
    console.log(data.selected);
      $.get('/ajax/omics-tag-description/', {'tag_name': data.selected[0]}, function(data){
         console.log('hahaha');
         $('#portal_tag').html(data);
        });

    if ( $('#container').jstree(true).is_open(data.node)){
      $('#container').jstree(true).close_node(data.node);

      }
      else {
    $('#container').jstree(true).open_node(data.node);
    }
  });

  $('#container').on('search.jstree', function (e, data) {
    console.log(data.res.length);
    if (data.res.length <= 1){
      $('#search-results').html("Found "+data.res.length+" match");
    }
    else {
    $('#search-results').html("Found "+data.res.length+" matches");
    }
  });

  $('#container').on('clear_search.jstree', function (e, data) {
    $('#search-results').html("");
  });


//  $('#container').on('deselect_node.jstree', function (e, data) {
//    console.log(data.event);
//    $('#container').jstree(true).close_node(data.node);
//  });

});



// send empty string initially so every tag would show up.
/*
var query = "";
$.get('/tags/suggest_tag/', {suggestion: query}, function(data){
         $('#tags').html(data);
        });

$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    console.log( query );
    $.get('/tags/suggest_tag/', {suggestion: query}, function(data){
         $('#tags').html(data);
        });
});
*/
