from django.shortcuts import render
from django.views.generic import TemplateView
from geopy.geocoders import Nominatim
# from geopy.distance import geodesic



# Creae your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):

        # addrees = print_addresses_from_pincode(700150)
        return render(self.request, self.template_name)
    
    