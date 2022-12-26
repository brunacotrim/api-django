from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):

    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    sku = filters.CharFilter(field_name='sku', lookup_expr='iexact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', lookup_expr='istartswith')
    enable = filters.BooleanFilter(field_name='status')
    updated_after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gt')
    variation = filters.CharFilter(field_name='variations__name', lookup_expr='iexact')
    variation_value = filters.CharFilter(field_name='variations__value', lookup_expr='iexact')

    has_brand = filters.BooleanFilter(field_name='brand', method='no_empty')
    has_description = filters.BooleanFilter(field_name='description', method='no_empty')
    on_sale = filters.BooleanFilter(field_name='special_price', method='gt_zero')
    in_stock = filters.BooleanFilter(field_name='quantity', method='gt_zero')

    def no_empty(self, queryset, name, value):
        lookup = '__'.join([name, 'exact'])
        if value == True:
            return queryset.exclude(**{lookup: ''})
        else:
            return queryset.filter(**{lookup: ''})


    def gt_zero(self, queryset, name, value):
        if value == True:
            lookup_expresion = 'gt'
        else:
            lookup_expresion = 'exact'

        lookup = '__'.join([name, lookup_expresion])
        return queryset.filter(**{lookup: 0})
