from rest_framework import serializers

from .models import Product, Variation


class VariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variation
        fields = [
            'id',
            'product',
            'name',
            'value',
            'status',
            'created_at',
            'updated_at'
        ]


class ProductSerializer(serializers.ModelSerializer):

    variations = VariationSerializer(many=True, read_only=True)

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
            'variations'
        ]