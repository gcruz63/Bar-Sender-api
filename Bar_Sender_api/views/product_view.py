from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from Bar_Sender_api.models import Product, Store, Category, Order
from Bar_Sender_api.serializers import (
    ProductSerializer, CreateProductSerializer, AddRemoveRecommendationSerializer)
from django.db.models import Q


class ProductView(ViewSet):
    def create(self, request):
        """Create a new product for the current user's store"""
        store = Store.objects.get(seller=request.auth.user)
        category = Category.objects.get(pk=request.data['categoryId'])
        try:
            product = Product.objects.create(
                name=request.data['name'],
                store=store,
                price=request.data['price'],
                description=request.data['description'],
                quantity=request.data['quantity'],
                category=category
            )
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Update a product"""
        category = Category.objects.get(pk=request.data['categoryId'])

        try:
            product = Product.objects.get(
                pk=pk, store__seller=request.auth.user)
            product.name = request.data['name']
            product.price = request.data['price']
            product.description = request.data['description']
            product.quantity = request.data['quantity']
            product.category = category
            product.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Delete a product"""
        try:
            product = Product.objects.get(
                pk=pk, store__my_user=request.auth.user)
            product.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get a list of all products"""
        products = Product.objects.all()

        number_sold = request.query_params.get('number_sold', None)
        category = request.query_params.get('category', None)
        order = request.query_params.get('order_by', None)
        direction = request.query_params.get('direction', None)
        name = request.query_params.get('name', None)

        if number_sold:
            products = products.annotate(
                order_count=Count('orders', filter=~Q(order_payment_type=None))
            ).filter(order_count__gte=number_sold)

        if order is not None:
            order_filter = f'-{order}' if direction == 'desc' else order
            products = products.order_by(order_filter)

        if category is not None:
            products = products.filter(category__id=category)

        if name is not None:
            products = products.filter(name__icontains=name)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Get a single product"""
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True)
    def add_to_order(self, request, pk):
        """Add a product to the current users open order"""
        try:
            product = Product.objects.get(pk=pk)
            order, _ = Order.objects.get_or_create(
                user=request.auth.user, completed_on=None, payment_type=None)
            order.products.add(product)
            return Response({'message': 'product added'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['delete'], detail=True)
    def remove_from_order(self, request, pk):
        """Remove a product from the users open order"""
        try:
            product = Product.objects.get(pk=pk)
            order = Order.objects.get(
                user=request.auth.user, completed_on=None)
            order.products.remove(product)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # @action(methods=['post'], detail=True)
    # def unlike(self, request, pk):
    #     """add store to like list"""
    #     user = request.auth.user
    #     product = Product.objects.get(pk=pk)
    #     product.liked_products.add()
    #     return Response({'message': "like added"}, status=status.HTTP_201_CREATED)

    # @action(methods=['post'], detail=True)
    # def unlike(self, request, pk):
    #     """remove store from like list"""
    #     user = request.auth.user
    #     product = Product.objects.get(pk=pk)
    #     product.liked_products.remove(user)
    #     return Response({'message': 'like removed'}, status=status.HTTP_204_NO_CONTENT)


#     @action(methods=['post'], detail=True, url_path='rate-product')
#     def rate_product(self, request, pk):
#         """Rate a product"""
#         product = Product.objects.get(pk=pk)

#         try:
#             rating = Rating.objects.get(
#                 customer=request.auth.user, product=product)
#             rating.score = request.data['score']
#             rating.review = request.data['review']
#             rating.save()
#         except Rating.DoesNotExist:
#             rating = Rating.objects.create(
#                 customer=request.auth.user,
#                 product=product,
#                 score=request.data['score'],
#                 review=request.data['review']
#             )

#         return Response({'message': 'Rating added'}, status=status.HTTP_201_CREATED)
# # Adding like to product

#     @action(methods=['post'], detail=True)
#     def like(self, request, pk):

#         try:
#             product = Product.objects.get(pk=pk)
#             user = request.auth.user

#             Like.objects.create(customer=user, product=product)

#             return Response({'message': 'Like added'}, status=status.HTTP_201_CREATED)
#         except Like.DoesNotExist as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
