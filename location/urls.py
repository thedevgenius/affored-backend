from django.urls import path
from .views import LocationListView

urlpatterns = [
    path('locations/', LocationListView.as_view(), name='location_list'),
    # path('categories/', CategoryListView.as_view(), name='category_list')
]
