from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestView.as_view(), name='dashboard'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('site/create/', views.CreateSiteCardView.as_view(), name='site-create'),
    path('site/<str:hash>/delete/', views.DeleteSiteCardView.as_view(), name='site-delete'),
    path('site/<str:hash>/', views.DetailSiteCardView.as_view(), name='site-detail'),
]
