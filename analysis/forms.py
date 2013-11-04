from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
#    user = forms.CharField()
#    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User


class CreateUser(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    class Meta:
        model = User

class SendMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':55, 'style':'width:inherit'}), label='', required=True)

