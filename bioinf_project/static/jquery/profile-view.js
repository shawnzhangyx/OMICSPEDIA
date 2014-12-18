$(document).ready(function() {

$('.profile-view-tab-choice').each( function(index){
    $(this).click( function(index){
    object = $(this).attr('target');
    console.log('#'+object);
    $('.profile-view-tab-choice').attr('class', 'profile-view-tab-choice profile-view-tab-choice-off');
    $(this).attr('class', 'profile-view-tab-choice profile-view-tab-choice-on');
    $('#profile-view-bookmark>div').css("display", "none");
    $('#'+object).css('display','block');
});
});

});
