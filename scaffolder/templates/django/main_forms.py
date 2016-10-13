from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserToken


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__' 


class UserTokenForm(ModelForm):
    class Meta:
        model = UserToken
        fields = '__all__' 
