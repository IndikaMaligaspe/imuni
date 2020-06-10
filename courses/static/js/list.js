(
 function($) {
    "use strict";

    // manual carousel controls
    $('.next').click(function(){ $('.carousel').carousel('next');return false; });
    $('.prev').click(function(){ $('.carousel').carousel('prev');return false; });
    $('#search_icon').click(function(e){
        console.log(e.target.id);
        $('.search-box').css({'display':'block'});
    });
    $('#search_box_close').click(function(e){
        $('.search-box').css({'display':'none'});
    });
    $('#search_box_input').keypress(function(e){
        console.log(e.target.value);

    });
    $('#search_box_button').click(function(){
        let value = $('#search_box_input').val();
        console.log(value);
        search(value);
    });
    $('#exampleModalLabel').on('shown.bs.modal', function () {
        $('#myInput').trigger('focus')
    });
})(jQuery);

// call search and get the load the results
search=(value)=>{
    console.log('inside test - '+value);
    console.log('BASE URL - '+SEARCH_URL);

}