from django.urls import path
from .views import UserSignUpView, UserSignInView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signin/', UserSignInView.as_view(), name='signin')
]
