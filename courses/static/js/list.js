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
        console.log($('#delete_course_form').attr('action'))
        $.post($('#delete_course_form').attr('action'), $('#delete_course_form').serialize(),function(data){
           $('#dashboard').html(data)
       });
       return false;
    });  
    $('#dashboard').on('click','#edit_course_modules',function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
        return false;
    });
    $('#dashboard').on('click','#edit_content',function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
        return false;
    });
    $('#dashboard').on('click','#add_text_content',function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
        return false;
    }); 
    $('#dashboard').on('click','#add_image_content',function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
        return false;
    });  
    $('#dashboard').on('click','#add_video_content',function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
        return false;
    });  
    $('#dashboard').on('click','#add_file_content',function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
        return false;
    });
    $('#dashboard').on('click','#load_dashboard',function(e){
        e.preventDefault;
        $('#dashboard').load($('#hid_load_dashboard').val());
        return false;
    });   
    $('#dashboard').on('submit','#submit_add_content',function(e){
        e.preventDefault;
        let img_data = '';
        let form = document.getElementById('submit_add_content');
        
        let formdata = new FormData(form);
        try{
             $.ajax(
                 {
                     url: $('#submit_add_content').attr('action'), 
                     data: formdata,
                     method: 'POST',
                     contentType: false,
                     processData: false,
                     success: function(data){
                 $('#dashboard').html(data)}
             })
        } catch (error) {
                console.log(error)    
        }
        return false;
     });  
     $('#dashboard').on('submit','#delete_module_content',function(e){
        e.preventDefault;
         $.post($('#delete_module_content').attr('action'), $('#delete_module_content').serialize(),function(data){
            $('#dashboard').html(data)
        });
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
     $('#id_account_page').click(function(e){
        e.preventDefault;
        $('#dashboard').load($(this).attr('href'));
           return false;
     }); 
     $('.list-group-item').click(function(e) {
        e.preventDefault();
        $('.list-group-item').removeClass('active');
        $(this).addClass('active');
      }); 
    $('#dashboard').on('click','#btn_add_module',function(e){
        e.preventDefault;

        console.log($('#id_modules-TOTAL_FORMS').val())
        let index = parseInt($('#id_modules-TOTAL_FORMS').val())+1;
        console.log(index)
        let html = '' 
        let title = gettext('Title')
        let description = gettext('Description')
        let duration = gettext('Duration')
        let delete_text = gettext('Delete')
        let add_content = gettext('Add Content')
        for (let i = index; i < index+3; i++) {
            html += `<div class='row bg-light'>
                        <div class="col">
                            <div class="row">
                                <div class="col-md-2 col-6">
                                    <label for="id_modules-`+i+`-title">`+title+`:</label>
                                </div>
                                <div class="col-md-8 col-6">
                                    <input type="text" name="modules-`+i+`-title" size="50" maxlength="200" id="id_modules-`+i+`-title">
                                </div>
                                <div class="col-md-1 col-6">
                                    <label for="id_modules-0-duration">`+duration+`:</label>
                                </div>
                                <div class="col-md-1 col-6">
                                    <input type="text" name="modules-`+i+`-duration" value="5" size="3" id="id_modules-`+i+`-duration">
                                </div>
                            </div> 

                            <div class="row">
                                <div class="col-md-2 col-3">
                                <label for="id_modules-`+i+`-description">`+description+`:</label>
                                </div>
                                <div class="col-md-9 col-9">
                                    <textarea name="modules-`+i+`-description" cols="83" rows="5" id="id_modules-`+i+`-description"></textarea>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-8"></div>
                                <div class="col-md-1 col-6 p-1">
                                    <label for="id_modules-`+i+`-DELETE">`+delete_text+`:</label>
                                </div>
                                <div class="col-md-1 col-6 p-1">
                                    <input type="checkbox" name="modules-`+i+`-DELETE" id="id_modules-`+i+`-DELETE">
                                </div>
                                <div class="col-md-2 col-6 p-1">
                                    <a href="">`+add_content+`</a>
                                </div>
                            </div>      
                        </div>
                    </div>   
                    <div class="row">
                        <div class="col">
                            <br>
                        </div>
                    </div>  
                </div>
            <div class="container" id="add_module_temp"></div>`;        
        }
    
        console.log(html) 
        $('#add_module').html(html)
        $('#add_module').prop("id","add_module_done");
        $('#add_module_temp').prop("id","add_module");
        return false;
     }); 
     $('#dashboard').on('submit','#submit_account_form',function(e){
        e.preventDefault;
         $.post($('#submit_account_form').attr('action'), $('#submit_account_form').serialize(),function(data){
            $('#dashboard').html(data)
        });
        return false;
     });
     $('#messageModel').modal({show:true});
    
    
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


load_content=(e)=>{
    id = e.target.id;
    console.log('taregt_id:'+id)
    module_id = $('#id_modules-'+id+'-id').val();
    load_content_page(module_id)
    return false;
}

load_content_select=(e)=>{
   load_content_page(e.target.value)
}
load_content_page=(module_id)=>{
    url = '/course/module/'+module_id;
    $('#dashboard').load(url);
    return false;   
}

// console.log(paid_filter);