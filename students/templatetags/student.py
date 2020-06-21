from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    retval = 'N/A'
    if  'key' in k:
        retval = d[0]
    else:
        retval = d[1]
    
    # print(f'--- {retval}')
    return retval
            
