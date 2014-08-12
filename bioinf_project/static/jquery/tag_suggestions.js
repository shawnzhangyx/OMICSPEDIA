$(document).ready(function() {

// send empty string initially so every tag would show up.
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

//$('body').tooltip({ selector:'[data-toggle=tooltip]'});


});


