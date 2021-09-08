from django.urls import path
from rest_framework import routers

# from rest_framework.authtoken.views import obtain_auth_token

from users.views import (
    GoogleValidateUserId, GoogleSignupAPIView,
    LoginView, UserViewSet
)

urlpatterns = [
    path(
        'google-id-validation/', GoogleValidateUserId.as_view(),
        name="google-id-validation"
    ),
    path('google/signup/', GoogleSignupAPIView.as_view(), name="google-signup"),
    # path('login/', obtain_auth_token, name='login'),
    path('login/', LoginView.as_view(), name='login'),
]

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns += router.urls
