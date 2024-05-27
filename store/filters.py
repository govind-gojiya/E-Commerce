from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'title': ['icontains'],
            'unit_price': ['gt', 'lt'],
            'collection_id': ['exact'],
        }