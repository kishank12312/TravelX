from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length = 250, help_text = 'You will need this to login')
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'datepicker'}))

    class Meta:
        model = Account
        fields = ('email','username','date_of_birth','password1','password2')
