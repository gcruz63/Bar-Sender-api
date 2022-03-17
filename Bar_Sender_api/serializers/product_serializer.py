from rest_framework import serializers
from Bar_Sender_api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description',
                  'quantity', 'image_path', 'category', 'store',
                  'number_purchased')
        depth = 1


class CreateProductSerializer(serializers.Serializer):
    categoryId = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=7)
    description = serializers.CharField()
    quantity = serializers.IntegerField()
    image = serializers.ImageField()


class AddRemoveRecommendationSerializer(serializers.Serializer):
    username = serializers.CharField()


# class AddProductRatingSerializer(serializers.Serializer):
#     score = serializers.IntegerField()
#     rating = serializers.CharField()
