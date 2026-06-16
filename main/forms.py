from django import forms
from django.contrib.auth.models import User
from .models import Profile, PortfolioImage

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    class Meta:
        model = User
        fields = ["username","email","password"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["role","name","age","gender","phone","profession","experience","domain","bio","photo"]

class PortfolioImageForm(forms.ModelForm):
    class Meta:
        model = PortfolioImage
        fields = ["image","caption"]
