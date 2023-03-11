from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomerCreationForm(UserCreationForm):
    '''Form for signup'''
    username = forms.EmailField(required = True , label = "Email")
    Username = forms.CharField(required = True , label = "Username")
    first_name = forms.CharField(required = True , label = "First Name")
    last_name = forms.CharField(required = True , label = "Last Name")
   
    def clean_first_name(self):   
        ''' validate first_name '''
        value = self.cleaned_data.get('first_name')
        if len(value.strip()) < 4:
            raise ValidationError("First Name must be 4 character long..")
        return value.strip()

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name')
        if len(value.strip()) < 4:
            raise ValidationError("First Name must be 4 character long..")
        return value.strip()

    class Meta:
        model = User
        fields = ['Username','username','first_name','last_name']
        # fields = ['first_name','last_name','username','name']


class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(required= True, label = "Username")

    class Meta:
        model = User
        fields = ['username']