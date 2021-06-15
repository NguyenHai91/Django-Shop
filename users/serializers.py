from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'full_name', 'email', 'phone']


class UserSerializerWithToken(UserSerializer):
  class Meta:
    model = User
    fields = ['id', 'full_name', 'email', 'phone']

  def get_token(self, obj):
    token = RefreshToken.for_user(obj)
    return str(token.access_token)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    data = super().validate(attrs)

    serializer = UserSerializerWithToken(self.user).data
    for k, v in serializer.items():
      data[k] = v
    return data

