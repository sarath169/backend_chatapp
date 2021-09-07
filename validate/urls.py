from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import ValidateUser, UserCreateAPIView, GenerateToken

urlpatterns = [
    path('validate/', ValidateUser.as_view(), name = "user_validation"),
    path('google/newuser/', UserCreateAPIView.as_view(), name = "new_user"),
    path('login/', obtain_auth_token, name = 'loign'),
    path('token/', GenerateToken.as_view(), name = 'token'),
]
