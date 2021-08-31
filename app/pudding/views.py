from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView, FormView, UpdateView, TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from . import forms
from . import models


class ListView(LoginRequiredMixin, TemplateView):
    template_name = 'pudding/forms/list.html';
    login_url = '/login/'

    def list_serializer(self, queryset):
        data = {}
        for site in queryset:
            data[str(site.card.pk)] = {
                'link': reverse('site-update', kwargs={'id': site.card.pk}),
                'title': site.host,
                'username': site.card.username
            }
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.list_serializer(
            models.SiteCard.objects.filter(
                card__owner=self.request.user,
                card__is_deleted=False
            )
        )
        return context


class RedirectAuthorizedUserMixin:
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.success_url is None:
                return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class RegistrationView(RedirectAuthorizedUserMixin, CreateView):
    template_name = 'auth/registration.html'
    form_class = forms.RegistrationForm
    success_url = '/'


class LoginView(RedirectAuthorizedUserMixin, FormView):
    template_name = 'auth/login.html'
    form_class = forms.LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)

    def get_initial(self):
        return {'next': self.request.GET.get('next')}

    def get_success_url(self):
        default_to = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        redirect_to = self.request.POST.get('next')

        url_is_save = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=settings.ALLOWED_HOSTS,
            require_https=settings.REQUIRE_HTTPS
        )

        ref = redirect_to if url_is_save else default_to
        return reverse('key') + '?next=' + ref


class LogoutView(View):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            getattr(settings, 'LOGOUT_REDIRECT_URL', '/')
        )


class KeyView(UpdateView):
    template_name = 'pudding/forms/key.html'
    form_class = forms.KeyForm
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        return {'next': self.request.GET.get('next')}

    def get_success_url(self):
        default_to = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        redirect_to = self.request.POST.get('next')

        url_is_save = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=settings.ALLOWED_HOSTS,
            require_https=settings.REQUIRE_HTTPS
        )

        return redirect_to if url_is_save else default_to


class SiteCardMixin:
    login_url = '/login/'
    form_class = forms.SiteCardForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('site-update', kwargs={'id': self.object.card.id})


class CreateSiteCardView(SiteCardMixin, LoginRequiredMixin, CreateView):
    template_name = 'pudding/sitecard/create.html'


class UpdateSiteCardView(SiteCardMixin, LoginRequiredMixin, UpdateView):
    template_name = 'pudding/sitecard/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            models.SiteCard,
            card__owner=self.request.user,
            card_id=self.kwargs['id'],
            card__is_deleted=False
        )

    def get_initial(self):
        return {
            'username': self.object.card.username,
            'password': self.object.card.password,
            'notes': self.object.card.notes,
            'is_favorite': self.object.card.is_favorite
        }


class DeleteSiteCardView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, **kwargs):
        return HttpResponseRedirect(reverse('site-update', kwargs={'id': kwargs['id']}))

    def post(self, request, **kwargs):
        models.Card.mark_as_deleted(owner=request.user, id=kwargs['id'])
        return HttpResponseRedirect(reverse('homepage'))
