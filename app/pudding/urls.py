from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListView.as_view(), name='homepage'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('key/', views.KeyView.as_view(), name='key'),
    path('site/create/', views.CreateSiteCardView.as_view(), name='site-create'),
    path('site/<uuid:id>/delete/', views.DeleteSiteCardView.as_view(), name='site-delete'),
    path('site/<uuid:id>/', views.UpdateSiteCardView.as_view(), name='site-update'),
]
