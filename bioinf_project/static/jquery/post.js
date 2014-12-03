$(document).ready(function() {

$('#wmd-input').keyup(function(){
    string = $(this).val();
    console.log(string);
    if (string.length < 20) {
    $('#content-string-count').html((20-string.length)+" more letters required to submit");
    $('#content-string-count').addClass("alert alert-info");
    }
    else {
    $('#content-string-count').html('');
     $('#content-string-count').removeClass("alert alert-info");
    }
});

});