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
    $('#dashboard').on('click','#create_course',function(e){
        e.preventDefaults;
        $('#dashboard').load($(this).attr('href'));
           return false;
   });
   $('#dashboard').on('click','#edit_course',function(e){
    e.preventDefaults;
    $('#dashboard').load($(this).attr('href'));
       return false;
    });
    $('#dashboard').on('click','#delete_course',function(e){
        e.preventDefaults;
        $('#dashboard').load($(this).attr('href'));
           return false;
    });    
   $('#dashboard').on('submit','#create_course_form',function(e){
        e.preventDefault;
        $.post($('#create_course_form').attr('action'), $('#create_course_form').serialize(),function(data){
            $('#dashboard').html(data)
        });
        return false;
    }); 
    $('#dashboard').on('submit','#delete_course_form',function(e){
       e.preventDefault;
        $.get($('#delete_course_form').attr('action'), $('#delete_course_form').serialize(),function(data){
           $('#dashboard').html(data)
       });
       return false;
    });  
    $('#dashboard').on('click','#edit_course_modules',function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
        return false;
    }); 
    $('#dashboard_course_list').click(function(e){
         e.preventDefault;
         $('#dashboard').load($(this).attr('href'));
            return false;
    });
    $('#dashboard').on('submit','#edit_modules',function(e){
        e.preventDefault;
         $.post($('#edit_modules').attr('action'), $('#edit_modules').serialize(),function(data){
            $('#dashboard').html(data)
        });
        return false;
     });  
    
    
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