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

    def validate(self, data):
        if data['special_price'] >= data['price']:
            raise serializers.ValidationError(
                'O preço promocional precisa ser menor que o preço do produto.')
        return data


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'quantity'
        ]


class OnSaleSerializer(serializers.ModelSerializer):

    discount = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'price',
            'special_price',
            'discount',
            'discount_percentage'
        ]

    def get_discount(self, data):
        return data.price - data.special_price

    def get_discount_percentage(self, data):
        return round(((data.price - data.special_price) / data.price) * 100, 2)