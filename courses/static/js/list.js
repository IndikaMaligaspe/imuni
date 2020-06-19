(

 function($) {
    "use strict";

    // manual carousel controls
    $('.next').click(function(){ $('.carousel').carousel('next');return false; });
    $('.prev').click(function(){ $('.carousel').carousel('prev');return false; });
    $('#language_selection').click(function (e) {
        console.log('hi')
    });
    $('.form-check-input').click(function (e) {
        console.log(e.target.id)
        let elem = $(this).prop('value');
        if(e.target.id == 'skill_level'){
           
            if($(this).prop("checked")== true){
                skill_level_filter[elem]='1';
            }else{
                skill_level_filter[elem]='0';
            }
        }else if (e.target.id == 'paid_filter'){
            if($(this).prop("checked")== true){
                paid_filter[elem] = '1';
            }else{
                paid_filter[elem] = '0';
            }         
        }else if (e.target.id == 'ratingOpt'){
                rating_filter=elem;
        }
        console.log(elem);
        console.log(elem.value);
        console.log(paid_filter)
        update_form();
    });
    // $('#addToCart').click(function(e){
    //    $('#id_course_id').val()
    //    $('#id_price').val()
    //    $('#id_discount').val()
    //    $('#id_coupon_code').val() 

    // });
    
})(jQuery);

// call search and get the load the results
update_form=()=>{
    let hid_skill_filter = ''; 
    let hid_paid_filter = '';
    // 
    $.each(skill_level_filter,function(key,val){
       console.log(key+' - '+val) 
       if(val === '1') {
         hid_skill_filter += key +","
       }
    }); 
    $.each(paid_filter,function(key,val){
        console.log(key+"--"+val)
        if(val === '1') {
            hid_paid_filter += key +","
        }
     });
    // console.log(rat)   
    $('#hid_skill_filter').val(hid_skill_filter);
    $('#hid_paid_filter').val(hid_paid_filter);
    $('#hid_ratind_filter').val(rating_filter);
    console.log($('#hid_skill_filter').val());
    
    $('#submit_frm').submit();  
    console.log($('#hid_ratind_filter').val());    
}



// console.log(paid_filter);