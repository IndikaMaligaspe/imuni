from django import forms

class CartAddForm(forms.Form):
    course_id = forms.CharField(max_length=50,widget=forms.HiddenInput())
    price = forms.CharField(max_length=50,widget=forms.HiddenInput())
    discount = forms.CharField(max_length=50,widget=forms.HiddenInput(),)
    coupon_code = forms.CharField(max_length=50,widget=forms.HiddenInput(),required=False)
    