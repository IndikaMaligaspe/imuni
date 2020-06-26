{% extends "mail_templated/base.tpl" %}
{% load staticfiles %}

{% block subject %}
   Order confirmed -  {{ user.first_name }}
{% endblock %}
   
{% block html %}
   <html>
      <head>
      <style>
         container {
            width: 100%;
            padding-right: 15px;
            padding-left: 15px;
            margin-right: auto;
            margin-left: auto;
         }
         row {
            display: -ms-flexbox;
            display: flex;
            -ms-flex-wrap: wrap;
            flex-wrap: wrap;
            margin-right: -15px;
            margin-left: -15px;
         }
         col {
            position: relative;
            width: 100%;
            padding-right: 15px;
            padding-left: 15px;
         }
      </style>
      </head>
      <body>
      <div class="container">
        <div class="row">
            <div class="col">
            <table>
               <tr>
                  <td><img src='http://{{ host }}/static/images/logo.png' style="width:150px;height:150px" alt=""> </td>
                  <td> <h2>IM-UNI - Lorem Ipsum</h2> </td>
               </tr>
            </table>   
            </div>
        </div>
        <div class="row">
           <table style="width:100%">
              <tr>
                 <td><h5> Order Confirmed for {{ order.order_by.first_name|title }} {{ order.order_by.last_name|title }} with order id {{ order.id}}</h5></td>
              </tr> 
           </table> 
        </div>
        <div class="row">
         <table style="width:100%">
            <tr><td> You registered for </td></tr>
            {% for item in order.items.all %}
              <tr>
                <td>{{item.course.title}} 
                    <span> by {{item.course.owner.first_name}} {{item.course.owner.last_name}}</span>  
                </td>
                <td><div class="col-md-4 col-2 p-0 text-right">${{item.price}}</div></td>
              </tr>   
            {% endfor %}
            <tr>
              <td>
                 <span> Total of {{cart.get_item_count}} item(s)</span>  
              </td>
              <td>${{order.get_total_cost}}</td> 
            </tr>
         </table> 
      </div>
      <h5>You might also like</h5>  
      
      <div class="row">
         <table>
            {% for course in courses  %}
            <tr>
               <td> <a href='http://{{ host }}/course/{{course.slug}}'>{{course.title}} by {{course.owner.first_name}}  {{course.owner.last_name}} @ $ {{course.price}}</a></td>
            </tr>
            {% endfor %}
         </table>
      </div>   
     </div> 
   </body>
</html>
{% endblock %}