from django.shortcuts import render
from apy.models import *
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apy.forms import *

class index(LoginRequiredMixin, TemplateView):
    template_name = 'body.html'
    login_url = reverse_lazy('login:login')
