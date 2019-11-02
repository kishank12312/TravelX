from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length = 250, help_text = 'You will need this to login')
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'datepicker inline'}))

    class Meta:
        model = Account
        fields = ('email','username','date_of_birth','password1','password2')

class LoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login details.Try again")
