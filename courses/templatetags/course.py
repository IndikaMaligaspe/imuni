from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name 
    except AttribueError:    
        return None

@register.filter
def highlight(text, word):
    return mark_safe(text.replace(word, "<span class='highlight'>%s</span>" % word))

@register.filter
def ratings(value):
    if value == None:
        value = 0
    # print('----------------------------{}'.format(value))
    
    str = ''
    x = int(value)
    for i in range(x):
        str+='<i class="fa fa-star-o fa-xs" aria-hidden="true"></i>'

    if isinstance(value,float):
        str+='<i class="fa fa-star-half-o fa-xs" aria-hidden="true"></i>'
    
    return mark_safe(str)


@register.filter
def makelist(text):
    # print("----------{}".format(text))
    return text.split(",");
        
        
