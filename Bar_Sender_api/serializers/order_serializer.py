from rest_framework import serializers
from Bar_Sender_api.models import Order
from Bar_Sender_api.models.payment_type import PaymentType
from .payment_type_serializer import PaymentTypeSerializer


class OrderSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer()

    class Meta:
        model = Order
        fields = ('id', 'products', 'created_on',
                  'completed_on', 'total', 'payment_type')
        depth = 1


class UpdateOrderSerializer(serializers.ModelSerializer):
    paymentTypeId = serializers.IntegerField()

    class Meta:
        model = PaymentType
        fields = ('paymentTypeId',)
