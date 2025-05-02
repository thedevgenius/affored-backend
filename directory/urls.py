from django.urls import path
from .views import CategoryAddView

urlpatterns = [
    path('category/add/', CategoryAddView.as_view(), name='category_add'),
    # path('signin/', UserSignInView.as_view(), name='signin')
]
