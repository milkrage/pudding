from django import forms
from django.core import validators
from django.contrib.auth import password_validation, get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from . import models


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    class Meta:
        model = models.User
        fields = ('email', )
        labels = {'email': _('Email address')}
        widgets = {'email': forms.EmailInput(attrs={'autofocus': True})}

    def clean_email(self):
        email = self.cleaned_data['email']

        if models.User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('The email is already in use.'), code='email_exists')

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError(_('Password mismatch'), code='password_mismatch')

        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password1')

        try:
            if isinstance(password, str):
                password_validation.validate_password(password, self.instance)
        except validators.ValidationError as error:
            self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )

    class Meta:
        model = models.User
        fields = ('email', )
        labels = {'email': _('Email address')}
        widgets = {'email': forms.EmailInput(attrs={'autofocus': True})}

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user = authenticate(self.request, email=email, password=password)

            if self.user is None:
                raise forms.ValidationError(_('Incorrect email or password.'), code='invalid_login')

            # authenticate возращает None, если поле is_active=False (user_can_authenticate).
            # Самостоятельная проверка user.is_active сделана из соображений перестраховки

            if not self.user.is_active:
                raise forms.ValidationError(_('This account is inactive.'), code='inactive')

        return self.cleaned_data
