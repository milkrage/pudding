from django.shortcuts import render
from django.views.generic import View, CreateView, FormView
from django.contrib.auth import login, logout
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from . import forms


class TestView(View):
    def get(self, request):
        username = request.user.email if request.user.is_authenticated else 'Anonymous'
        return render(request, 'pudding/test_page.html', context={'username': username})


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
