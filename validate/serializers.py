from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('user','social_login_source',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.save()
        return user