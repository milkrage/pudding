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


def test_view(request):
    """ Временное тестовое View, для отладки """
    username = request.user.email if request.user.is_authenticated else 'Anonymous'
    sites = models.SiteCard.objects.filter(card__is_deleted=False)
    trash = range(300)

    return render(
        request,
        'pudding/test_page.html',
        context={'username': username, 'sites': sites, 'count': range(300)}
    )


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
    form_class = forms.SiteCardForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['is_deleted'] = False
        return kwargs

    def get_success_url(self):
        return reverse('site-update', kwargs={'id': self.object.card.id})


class UpdateSiteCardMixin(SiteCardMixin):
    def get_object(self):
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


class CreateSiteCardView(SiteCardMixin, CreateView):
    template_name = 'pudding/sitecard/create.html'


class UpdateSiteCardView(UpdateSiteCardMixin, UpdateView):
    template_name = 'pudding/sitecard/update.html'


class DeleteSiteCardView(View):
    def get(self, request, **kwargs):
        return HttpResponseRedirect(reverse('site-update', kwargs={'id': kwargs['id']}))

    def post(self, request, **kwargs):
        models.Card.mark_as_deleted(owner=request.user, id=kwargs['id'])
        return HttpResponseRedirect(reverse('homepage'))
