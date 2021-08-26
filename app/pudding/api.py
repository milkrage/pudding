from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.auth import login, logout, get_user_model
from django.urls import reverse
from . import serializers
from . import models


class Registration(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer


class Login(APIView):
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            login(self.request, serializer.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_302_FOUND)


class Key(APIView):
    permission_classes = (IsAuthenticated, )

    def user_exist(self, request):
        query = get_user_model().objects.filter(email=request.user, is_active=True).exists()

        if query:
            return get_user_model().objects.get(email=request.user, is_active=True)

        return False

    def get(self, request):
        user = self.user_exist(request)

        if user:
            return Response({'cipher': user.cipher}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = serializers.KeySerializer(data=request.data)

        if serializer.is_valid():
            user = self.user_exist(request)
            if user:
                user.cipher = serializer.data['cipher']
                user.save()
                return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Sites(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SiteSerializer

    def get(self, request):
        result = {}

        for item in self.get_queryset():
            key = str(item.card.id)
            result[key] = {
                'link': reverse('site-update', kwargs={'id': key}),
                'title': item.host,
                'username': item.card.username
            }

        return Response(result, status=status.HTTP_200_OK)

    def get_queryset(self):
        return models.SiteCard.objects.filter(card__owner=self.request.user, card__is_deleted=False)


class SiteCard(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SiteSerializer
    queryset = models.SiteCard.objects.all()
    lookup_field = 'card__id' # в query.filter(card__id=x)
    lookup_url_kwarg = 'id'   # в query.filter(lookup_field=id)

    def get_queryset(self):
        return models.SiteCard.objects.filter(card__owner=self.request.user, card__is_deleted=False)

    def perform_destroy(self, instance):
        instance.card.is_deleted = True
        instance.card.save()
