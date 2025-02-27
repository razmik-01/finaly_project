from django import forms
from .models import CustomUser


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
