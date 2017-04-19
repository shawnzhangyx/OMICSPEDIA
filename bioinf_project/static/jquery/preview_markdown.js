$(document).ready(function() {

$('#preview-click').click(function(){
    var content;
    content = $('#wmd-input').val();
    $.post('/ajax/preview-markdown/', {content: content}, function(data){
         $('#preview-mkd-text').html(data);
        });
});


});


