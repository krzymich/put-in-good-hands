from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class RegisterForm(ModelForm):
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło', 'autocomplete': 'new-password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwsko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Hasło', 'autocomplete': 'new-password'}),
        }
        error_messages = {
            'email': {
                'invalid': _('Wprowadź poprawne dane'),
                'required': _('Pole wymagane'),
            }
        }

    def clean(self):
        # cleaned_data = super(RegisterForm, self).clean()
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password_confirmation', ValidationError(_("Wprowadzone hasła nie są identyczne")))
