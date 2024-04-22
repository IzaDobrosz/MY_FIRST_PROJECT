from django.shortcuts import render
from django.contrib.auth.views import LoginView


class MyGardenLoginView(LoginView):
    template_name = 'registration/login.html'
