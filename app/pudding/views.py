from django.shortcuts import render
from django.views import View


class TestView(View):
    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'Anonymous'
        return render(request, 'pudding/test_page.html', context={'username': username})


