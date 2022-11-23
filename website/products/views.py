from .serializers import ProductSerializer
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from .models import Product
from .filters import ProductFilter


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
