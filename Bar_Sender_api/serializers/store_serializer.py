from rest_framework import serializers
# from django.contrib.auth.models import User
from Bar_Sender_api.models import Store
from Bar_Sender_api.models.my_user import MyUser


class StoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('__all__')


class StoreSerializer(serializers.ModelSerializer):
    my_user = StoreUserSerializer()
    # is_favorite = serializers.BooleanField(required=False)

    class Meta:
        model = Store
        fields = ('id', 'name', 'description', 'products', 'my_user')
        depth = 1


class AddStoreSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
