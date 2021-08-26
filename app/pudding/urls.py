from django.urls import path
from django.conf import settings
from . import views
from . import api

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

if settings.API_ENABLE:
    urlpatterns += [
        path('api/registration/', api.Registration.as_view()),
        path('api/login/', api.Login.as_view()),
        path('api/logout/', api.Logout.as_view()),
        path('api/key/', api.Key.as_view()),
        path('api/sites/<uuid:id>/', api.SiteCard.as_view()),
        path('api/sites/', api.Sites.as_view()),
    ]