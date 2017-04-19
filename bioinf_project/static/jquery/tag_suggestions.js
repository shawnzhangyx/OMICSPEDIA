$(document).ready(function() {

// send empty string initially so every tag would show up.


$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    //console.log( query );
    $.get('/tags/suggest_tag/', {suggestion: query}, function(data){
         
         console.log(query);
         if (query == '') {
         $('.pagination').css("display", "block");
         $('#tag-default').css("display", 'block');
         $('#tags').html('');

         }
         else { 
         $('#tag-default').css("display", 'none');
         $('.pagination').css("display", "none");
         $('#tags').html(data);
         }
        });
});


});


