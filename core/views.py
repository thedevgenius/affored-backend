from django.shortcuts import render
from django.views.generic import TemplateView

# Creae your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'
    