# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=u'名字',required=False)
    email = forms.EmailField(label=u'电子邮件*',help_text=u'请输入正确电子邮件用于找回密码。')
    error_css_class = 'error'
    required_css_class = 'required'
    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data["username"], self.cleaned_data["email"], self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.Form):
    """
    A form that update a user information
    """
    first_name = forms.CharField(label=u'名字',required=False)
    email = forms.EmailField(label=u'电子邮件*',help_text=u'请输入正确电子邮件用于找回密码。')
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()
        return self.user
