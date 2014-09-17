$(document).ready(function() {

$('#preview-click').click(function(){
    var content;
    content = $('#wiki_text').val();
    console.log(content);
    $.get('/ajax/preview-markdown/', {content: content}, function(data){
         $('#preview-mkd-text').html(data);
        });
});


});


