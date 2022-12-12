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
    