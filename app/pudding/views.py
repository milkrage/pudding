from django.shortcuts import render
from django.views.generic import View, CreateView
from . import forms


class TestView(View):
    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        return render(request, 'pudding/test_page.html', context={'username': username})


class RegistrationView(CreateView):
    template_name = 'auth/registration.html'
    form_class = forms.RegistrationForm
    success_url = '/'
