from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestView.as_view()),
    path('registration/', views.RegistrationView.as_view()),
]
