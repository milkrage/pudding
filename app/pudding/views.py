from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView, FormView, UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from . import forms
from . import models


class TestView(View):
    def get(self, request):
        username = request.user.email if request.user.is_authenticated else 'Anonymous'
        sites = models.SiteCard.objects.filter(owner=request.user.id)
        return render(request, 'pudding/test_page.html', context={'username': username, 'sites': sites})


class RedirectAuthorizedUserMixin:
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class RegistrationView(RedirectAuthorizedUserMixin, CreateView):
    template_name = 'auth/registration.html'
    form_class = forms.RegistrationForm
    success_url = '/'


class LoginView(RedirectAuthorizedUserMixin, FormView):
    template_name = 'auth/login.html'
    form_class = forms.LoginForm
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class LogoutView(View):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            getattr(settings, 'LOGOUT_REDIRECT_URL', '/')
        )


class SiteCardMixin:
    login_url = 'login'
    form_class = forms.SiteCardForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('site-detail', kwargs={'hash': self.object.hash})


class CreateSiteCardView(SiteCardMixin, LoginRequiredMixin, CreateView):
    """ /site/create/  method CRUD: create """
    template_name = 'pudding/sitecard.html'


class DetailSiteCardView(SiteCardMixin, LoginRequiredMixin, UpdateView):
    """ /site/<str:hash>/  method CRUD: read + update """
    template_name = 'pudding/sitecard_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(models.SiteCard, owner=self.request.user.id, hash=self.kwargs['hash'])


class DeleteSiteCardView(LoginRequiredMixin, View):
    """ /site/<str:hash>/delete/  method CRUD: delete """
    login_url = 'login'

    def get(self, request, **kwargs):
        self.post(request, **kwargs)

    def post(self, request, **kwargs):
        obj = get_object_or_404(models.SiteCard, owner=request.user.id, hash=kwargs['hash'])
        obj.delete()
        return HttpResponseRedirect(reverse('dashboard'))
