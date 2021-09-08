from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

# from users.models import UserSocialAccount

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        """
        Check that user does not exists with the email.
        """
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )
        return data

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.save()
        # create token for the user
        Token.objects.get_or_create(user=user)
        return user


class UserSocialAccountSerializer(UserCreateSerializer):
    """
    """
    account_type = serializers.CharField()
    account_id = serializers.CharField(max_length=1024)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'account_type',
                  'account_id',)

    def create(self, validated_data):
        """
        Create user object first and then create his/her social account.
        """
        account_id = validated_data.pop("account_id", "")
        account_type = validated_data.pop("account_type", "")

        social_account_data = {
            "account_type": account_type,
            "account_id": account_id
        }

        user = super().create(validated_data)
        self.create_social_account(user, social_account_data)
        return user

    def create_social_account(self, user, social_account_data):
        """
        Create user's social account if signed up through social platform
        """
        social_account = UserSocialAccount.objects.create(
            user=user, **social_account_data)
        return social_account


class AuthTokenSerializer(serializers.Serializer):
    """
    """
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
