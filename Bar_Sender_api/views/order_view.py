from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from Bar_Sender_api.models import Order, PaymentType
from Bar_Sender_api.serializers import OrderSerializer, UpdateOrderSerializer


class OrderView(ViewSet):

    def list(self, request):
        """Get a list of the current users orders
        """
        orders = Order.objects.filter(user=request.auth.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Delete an order, current user must be associated with the order to be deleted
        """
        try:
            order = Order.objects.get(pk=pk, user=request.auth.user)
            order.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=True)
    def complete(self, request, pk):
        """Complete an order by adding a payment type and completed data
        """
        try:
            order = Order.objects.get(pk=pk, user=request.auth.user)
            payment_type = PaymentType.objects.get(
                pk=request.data['payment_type'], customer=request.auth.user)
            order.payment_type = payment_type
            order.completed_on = datetime.now()
            order.save()
            return Response({'message': "Order Completed"}, status=status.HTTP_204_NO_CONTENT)
        except (Order.DoesNotExist, PaymentType.DoesNotExist) as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def current(self, request):
        """Get the user's current order"""
        try:
            order = Order.objects.get(
                completed_on=None, user=request.auth.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({
                'message': 'You do not have an open order. Add a product to the cart to get started'},
                status=status.HTTP_404_NOT_FOUND
            )
