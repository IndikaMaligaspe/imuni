from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profiles


User = get_user_model()

class ProfileForm(ModelForm):
    class Meta:
        model = Profiles
        fields = {
            'bio','photo','city','country','email_display',\
                'webpage','phone','mobile','address','language',
        }