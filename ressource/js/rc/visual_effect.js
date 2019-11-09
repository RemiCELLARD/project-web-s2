$(document).ready(function(){
    $('input[name=actionDB]').on('change', function() {
        $(".js_visual_showElement").fadeToggle();
    });
});