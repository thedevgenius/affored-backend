from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import requests

api_key = settings.GOOGLE_MAP_API_KEY

def get_localities_from_pincode(pincode, api_key):
    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={pincode}&components=country:IN&key={api_key}"
    )
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        localities = set()
        for result in data.get("results", []):
            for comp in result.get("address_components", []):
                if "locality" in comp["types"] or "sublocality" in comp["types"]:
                    localities.add(comp["long_name"])
        return list(localities)
    else:
        return f"Error: {response.status_code} - {response.text}"









class LocationListView(TemplateView):
    template_name = 'location/location_list.html'
    def post(self, *args, **kwargs):
        pincode = self.request.POST.get('pincode')
        
        return render(self.request, self.template_name)
        

    