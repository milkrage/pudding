from rest_framework import serializers
from rest_framework import validators as drf_validators
from django.core import validators as django_validators
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.utils.translation import gettext_lazy as _
from . import models


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[
            drf_validators.UniqueValidator(
                queryset=get_user_model().objects.all(),
                message=_('The email is already in use.')
            )
        ]
    )
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        try:
            user = get_user_model()(email=data['email'])
            password_validation.validate_password(data['password'], user)
        except django_validators.ValidationError as error:
            raise serializers.ValidationError({'password': error})

        return data

    def create(self, validated_data):
        return get_user_model().objects.create_user(validated_data['email'], validated_data['password'])


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            self.user = authenticate(request=self.context['request'], email=data['email'], password=data['password'])

            if self.user is None:
                raise serializers.ValidationError(_('Incorrect email or password.'))

            if not self.user.is_active:
                raise serializers.ValidationError(_('This account is inactive.'))

        return data


class KeySerializer(serializers.Serializer):
    cipher = serializers.CharField(max_length=44)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ('id', 'username', 'password', 'notes', 'is_favorite')


class SiteSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = models.SiteCard
        fields = ('card', 'uri', 'host')

    def create(self, validated_data):
        card = models.Card(
            owner=self.context['request'].user,
            username=validated_data['card']['username'],
            password=validated_data['card']['password'],
            notes=validated_data['card']['notes'],
            is_favorite=validated_data['card']['is_favorite'],
        )
        card.save()

        sitecard = models.SiteCard(
            uri=validated_data['uri'],
            host=validated_data['host'],
            card=card,
        )
        sitecard.save()

        return sitecard

    def update(self, instance, validated_data):
        instance.card.username = validated_data['card'].get('username', instance.card.username)
        instance.card.password = validated_data['card'].get('password', instance.card.password)
        instance.card.notes = validated_data['card'].get('notes', instance.card.notes)
        instance.card.is_favorite = validated_data['card'].get('is_favorite', instance.card.is_favorite)
        instance.card.save()

        instance.uri = validated_data.get('uri', instance.uri)
        instance.host = validated_data.get('host', instance.host)
        instance.save()

        return instance

