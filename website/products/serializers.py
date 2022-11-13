from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'ean',
            'description',
            'brand',
            'warranty_time',
            'height',
            'width',
            'length',
            'weight',
            'price',
            'special_price',
            'quantity',
            'category',
            'status',
            'created_at',
            'updated_at',
        ]