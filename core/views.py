from django.shortcuts import render
from django.views.generic import TemplateView
import pygeohash as pgh

# Creae your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        geohash = pgh.encode(22.5111205, 88.3493046, 12)
        print(geohash)
        return render(self.request, self.template_name)
    
    