$(document).ready(function() {
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
});
