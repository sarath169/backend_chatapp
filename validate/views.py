import os
import time
import json

from dotenv import load_dotenv
import redis

from google.oauth2 import id_token
from google.auth.transport import requests

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from .models import MyUser

# Create your views here.
load_dotenv()

class ValidateUser(APIView):
    
# (Receive token by HTTPS POST)
# ...
    def get(self, request):
        print(request, "*******************8")
        token = request.query_params['token']
        CLIENT_ID = os.getenv('clientid')
        try:
        # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID )
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
            return Response({'user' : userid}, status= HTTP_200_OK)
        except ValueError:
        # Invalid token
            return Response({"error" : "error"}, status= HTTP_400_BAD_REQUEST)
        
class UserCreateAPIView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class LogoutView(APIView):
        # This view is to logout uers
        def get(self, request, format=None):
                try:
                        # simply delete the token to force a login
                        request.user.auth_token.delete()
                        data = {"message":"logout success"}
                        return Response(data, status=status.HTTP_200_OK)
                except:
                        message = {"message" : "Token not found" }
                        return Response(message, status=status.HTTP_404_NOT_FOUND)

class GenerateToken(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            user = authenticate(username = 'sarath', password = '12345')
        except Exception as e:
            print(e)
        token, _ = Token.objects.get_or_create(user = user)
        print(json.dumps(token.key))
        return Response({'token' : token.key}, status=HTTP_200_OK)
        

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
