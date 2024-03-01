from django import forms
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'phone', 'password', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'user_type': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['user_type'] = 'admin'