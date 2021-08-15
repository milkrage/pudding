from django import forms
from django.core import validators
from django.contrib.auth import password_validation, get_user_model, authenticate
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

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

    next = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = models.User
        fields = ('email', )
        labels = {'email': _('Email address')}
        widgets = {'email': forms.EmailInput(attrs={'autofocus': True})}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
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


class CardForm(forms.ModelForm):
    username = forms.CharField(
        label=_('Username'),
        max_length=254,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    password = forms.CharField(
        label=_('Password'),
        max_length=254,
        widget=forms.TextInput(attrs={'autocomplete': 'new-password', 'type': 'password', 'class': 'input-left'})
    )
    notes = forms.CharField(
        label=_('Notes'),
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False
    )
    is_favorite = forms.BooleanField(
        label=_('Favorite'),
        label_suffix='',
        widget=forms.CheckboxInput(),
        required=False
    )

    class Meta:
        model = models.Card
        fields = ('username', 'password', 'notes', 'is_favorite')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class SiteCardForm(CardForm):
    uri = forms.CharField(label=_('URI'), max_length=254, widget=forms.HiddenInput())
    host = forms.CharField(label=_('Host'), max_length=254, widget=forms.HiddenInput())

    class Meta:
        model = models.SiteCard
        fields = ('host', 'uri')

    def check_unique(self):
        """ Предполагается, что у одного пользователя (owner) не может быть два одинаковых username на одном uri """
        owner = self.request.user
        username = self.cleaned_data.get('username')
        uri = self.cleaned_data.get('uri')

        if not models.SiteCard.check_unique(owner, username, uri):
            query = models.SiteCard.objects.get(
                card__owner=owner,
                card__username=username,
                uri=uri,
                card__is_deleted=False
            )

            message = format_html(
                'Entry already exists: <br> <a href="{href}">{id}</a>'.format(
                    href=reverse('site-update', kwargs={'id': query.card.id}),
                    id=query.card.id
                )
            )
            raise forms.ValidationError(message, code='already_exists')

    def clean(self):
        # form action: create
        if self.instance.pk is None:
            self.check_unique()

        return super().clean()

    def save(self, commit=True):
        if self.errors:
            return super().save()

        card_fields = set(self.cleaned_data.keys()) - set(self.Meta.fields)
        card_data = {field: self.cleaned_data[field] for field in card_fields}

        # form action: update object
        if self.instance._state.adding is False:
            self.instance.save()
            models.Card.objects.filter(id=self.instance.card.id).update(**card_data)

        # form action: create object
        if self.instance._state.adding is True:
            card = models.Card.objects.create(owner=self.request.user, **card_data)
            self.instance.card = card
            self.instance.save()

        return self.instance

