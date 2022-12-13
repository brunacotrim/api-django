from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from decimal import Decimal

from .models import Product
from .filters import ProductFilter


CUBIC_FACTOR = Decimal('6000.0')
CORREIOS_MIN_LENGTH = Decimal('15.0')
CORREIOS_MIN_WIDTH = Decimal('10.0')
CORREIOS_MIN_HEIGHT = Decimal('1.0')
CORREIOS_MAX_DIMENSION = Decimal('100.0')
CORREIOS_SUM_DIMENSION = Decimal('200.0')
CORREIOS_MAX_WEIGHT = Decimal('30.0')


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
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
        

    @action(detail=True, methods=['get'], url_path='cubage', url_name='cubage')
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
    
    @action(detail=True, methods=['get'], url_path='correios', url_name='correios')
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
