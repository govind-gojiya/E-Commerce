from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Generic is concrete class which combine one or more mixins into one 
# mixins are used to replace repeated patterns like ListMixin, CreateMixin
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    # If we want to write complex querset which dependens on the request then override get_queryset instead of attribute querset 
    def get_queryset(self):
        return Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request}) # Passing request as context for hyperlink not for any other.
        return Response(serializer.data)

    # If we serializer which dependens on the request conditions then override get_serializer_class instead of attribute serializer_class 
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'id' # by default it's pk so you can change it according to
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': "Product can't be deleted due to it associated with order items."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionDetail(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('product'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
        if collection.product_set.count() > 0:
            return Response({'error': "Collection can't be deleted due to it associated with one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer
