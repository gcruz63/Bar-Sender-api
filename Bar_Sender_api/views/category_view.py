from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from Bar_Sender_api.models import Category
from Bar_Sender_api.serializers import CategorySerializer


class CategoryView(ViewSet):

    def list(self, request):
        """Get a list of categories
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
