from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from decimal import Decimal
from django.db.models import Count

from .serializers import *
from .models import Product, Variation
from .filters import ProductFilter


CUBIC_FACTOR = Decimal('6000.0')
CORREIOS_MIN_LENGTH = Decimal('15.0')
CORREIOS_MIN_WIDTH = Decimal('10.0')
CORREIOS_MIN_HEIGHT = Decimal('1.0')
CORREIOS_MAX_DIMENSION = Decimal('100.0')
CORREIOS_SUM_DIMENSION = Decimal('200.0')
CORREIOS_MAX_WEIGHT = Decimal('30.0')


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().distinct()
    serializer_class = ProductSerializer

    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering = ['-created_at']
    ordering_fields = [
        'sku',
        'name',
        'price',
        'special_price',
        'created_at',
        'updated_at',
        'special_price'
        ]

    @action(detail=True)
    def cubage(self, request, pk=None):
        data = self.get_object()
        cubed_weight = (data.height * data.width * data.length) / CUBIC_FACTOR

        if cubed_weight > data.weight:
            cubage = cubed_weight
        else:
            cubage = data.weight

        return Response({'cubage': round(cubage, 3),
                        'cubed_weight': round(cubed_weight, 3),
                        'real_weight': data.weight,
                        'cubic_factor': CUBIC_FACTOR})
    
    @action(detail=True)
    def correios(self, request, pk=None):
        data = self.get_object()
        details = {}
        response = {'available':False}

        product_sum_dimension = data.height + data.width + data.length
        if product_sum_dimension > CORREIOS_SUM_DIMENSION:
            details['product_sum_dimension'] = product_sum_dimension
            details['correios_sum_dimension'] = CORREIOS_SUM_DIMENSION
        
        if data.length < CORREIOS_MIN_LENGTH or data.length > CORREIOS_MAX_DIMENSION:
            details['product_length'] = data.length
            details['correios_min_length'] = CORREIOS_MIN_LENGTH
            details['correios_max_length'] = CORREIOS_MAX_DIMENSION

        if data.width < CORREIOS_MIN_WIDTH or data.width > CORREIOS_MAX_DIMENSION:
            details['product_width'] = data.width
            details['correios_min_width'] = CORREIOS_MIN_WIDTH
            details['correios_max_width'] = CORREIOS_MAX_DIMENSION

        if data.height < CORREIOS_MIN_HEIGHT or data.height > CORREIOS_MAX_DIMENSION:
            details['product_height'] = data.height
            details['correios_min_height'] = CORREIOS_MIN_HEIGHT
            details['correios_max_height'] = CORREIOS_MAX_DIMENSION
        
        if data.weight > CORREIOS_MAX_WEIGHT:
            details['product_weight'] = data.weight
            details['correios_max_weight'] = CORREIOS_MAX_WEIGHT
        
        if len(details) == 0:
            response['available'] = True
        else:
            response['details'] = details

        return Response(response)
    
    @action(detail=False,
        serializer_class = InventorySerializer,
        permission_classes = [permissions.IsAuthenticated])
    def inventory(self, request, pk=None):

        data = Product.objects.order_by('-quantity')
        return paginate_serializate(self, data)
    
    @action(detail=False,
        serializer_class = OnSaleSerializer,
        permission_classes = [permissions.IsAuthenticated])
    def onsale(self, request, pk=None):
        
        data = Product.objects.filter(special_price__gt=0)
        return paginate_serializate(self, data)

    @action(detail=False)
    def category(self, request, pk=None):
        
        data = Product.objects.values('category').annotate(
            products=Count('id')).order_by('-products')
        return Response(data)


class VariationViewSet(viewsets.ModelViewSet):

    queryset = Variation.objects.all()
    serializer_class = VariationSerializer


def paginate_serializate(self, data):
    page = self.paginate_queryset(data)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(data, many=True)
    return Response(serializer.data)
