$(document).ready(function() {

// this could enable tooltip on generated elements 
$('body').tooltip({ selector:'[data-toggle=tooltip]'});

$("#id_tags").select2();

var tagval = $("#id_tag_val")


/*
if (tagval.length > 0) {
    tagval.removeClass("textinput textInput form-control")
    tagval.width("96%")
     var tag_list = $.ajax({
        url: "/ajax/tags/",
        dataType: 'json',
        success: function (response) {
            tagval.select2({
                tags: response
            });
        }
    });
}
    */
});
