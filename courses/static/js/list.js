(
 function($) {
    "use strict";

    // manual carousel controls
    $('.next').click(function(){ $('.carousel').carousel('next');return false; });
    $('.prev').click(function(){ $('.carousel').carousel('prev');return false; });
    $('#language_selection').click(function (e) {
        console.log('hi')
    });
    
})(jQuery);

// call search and get the load the results
search=(value)=>{
    console.log('inside test - '+value);
    console.log('BASE URL - '+SEARCH_URL);

}