from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.forms import ModelForm

from .models import *

#extending usercreationform
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        #adding the email field
        fields = UserCreationForm.Meta.fields + ("email",)

class HobbyForm(forms.ModelForm):
    class Meta:
        model=Hobby
        fields=['hobbyname']