from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'orders',
                  'store', 'account_type')
        depth = 1


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    account_type = serializers.CharField()
