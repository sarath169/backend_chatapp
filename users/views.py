import os
import time
import json
import redis

from dotenv import load_dotenv

from google.oauth2 import id_token
from google.auth.transport import requests

from django_redis import get_redis_connection

from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    UserSocialAccountSerializer, AuthTokenSerializer, UserCreateSerializer
)

User = get_user_model()

# Create your views here.
load_dotenv()


class GoogleValidateUserId(APIView):
    """
        # (Receive token by HTTPS POST)
    """
    def get(self, request):
        token = request.query_params['token']
        CLIENT_ID = os.getenv('clientid')
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), CLIENT_ID
            )
            print(idinfo, "!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            print(userid)
            return Response({'user': userid}, status=status.HTTP_200_OK)
        except ValueError:
            # Invalid token
            return Response(
                {"error": "error"}, status=status.HTTP_400_BAD_REQUEST
            )


class GoogleSignupAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSocialAccountSerializer
    permission_classes = (AllowAny,)


class LogoutView(APIView):
    # This view is to logout uers
    def get(self, request, format=None):
        try:
            # simply delete the token to force a login
            request.user.auth_token.delete()
            data = {"message": "logout success"}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print("exception: ", e)
            message = {"message": "Token not found"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        }, status=status.HTTP_200_OK)

    # def get(self, request):
    #     try:
    #         user = authenticate(username = 'sarath', password = '12345')
    #     except Exception as e:
    #         print(e)
    #     token, _ = Token.objects.get_or_create(user = user)
    #     print(json.dumps(token.key))
    #     return Response({'token' : token.key}, status=status.HTTP_200_OK)
        

# r = redis.Redis(host = 'localhost', port=6379, db=0 )

# user1 = r.pubsub(ignore_subscribe_messages=True)
# user2 = r.pubsub(ignore_subscribe_messages=True)
# user3 = r.pubsub(ignore_subscribe_messages=True)

# def subscribe():
#     user1.subscribe('team1', 'team2')
#     user2.psubscribe('team*')
#     user3.subscribe('team3')

# subscribe()

# def publish():
#     r.publish('team1', 'Hi team 1')
#     r.publish('team2', 'Hi Team 2')
#     r.publish('team3', 'Hi Team 3')

# publish()
# def messages():
#     while True:
#         u1message = user1.get_message()
#         u2message = user2.get_message()
#         u3message = user3.get_message()

#         if u1message:
#             print("user1 : ", u1message)
#         if u2message:
#             print("user2 : ", u2message)
#         if u3message:
#             print("user3 : ", u3message)
        
#         time.sleep(0.001)
        

# messages()

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
