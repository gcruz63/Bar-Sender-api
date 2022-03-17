from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
# from django.db.models import Q, Count

from Bar_Sender_api.models import Store
from Bar_Sender_api.serializers import StoreSerializer, AddStoreSerializer


class StoreView(ViewSet):
    def create(self, request):
        """Create a store for the current user"""
        try:
            store = Store.objects.create(
                my_user=request.auth.user,
                name=request.data['name'],
                description=request.data['description']
            )
            serializer = StoreSerializer(store)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Get a list of all stores"""
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk):
    #     """Get a single store"""
    #     try:
    #         store = Store.objects.annotate(is_favorite=Count(
    #             'favorites',
    #             filter=Q(favorites=request.auth.user)
    #         )).get(pk=pk)
    #         serializer = StoreSerializer(store)
    #         return Response(serializer.data)
    #     except Store.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Update a store"""
        try:
            store = Store.objects.get(pk=pk)
            store.name = request.data['name']
            store.description = request.data['description']
            store.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Store.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
