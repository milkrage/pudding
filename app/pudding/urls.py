from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestView.as_view()),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]