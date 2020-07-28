from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import TextInput, Textarea, ImageField, ModelChoiceField
from .models import Profiles


User = get_user_model()

# ProfileForm = inlineformset_factory(User, Profiles, 
#                                     fields=['all'],      
#                                              can_delete=True)



class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'email'}
        widgets = {
            'first_name': TextInput(attrs={'size':'50'}),
            'last_name': TextInput(attrs={'size':'50'}),
            'email': TextInput(attrs={'size':'50'})
        }

class ProfileForm(ModelForm):
    class Meta:
        model =  Profiles
        fields = {'bio','photo','city','country','email_display',\
            'webpage','phone','mobile','address','language'
        }
        labels = {
           'email_display':'Email display' 
        }
        widgets = {
            'bio': Textarea(attrs={'row':'5', 'cols':'83'}),
        }

   