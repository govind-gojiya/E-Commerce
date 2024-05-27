from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .filters import ProductFilter
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, ProductImage, Review
from .pagination import ProductPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermission, ViewCustomerHistoryPermission
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer


# Viewset combine create, retrieve, update and destroy views in one
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    # filterset_fields = ('title', 'price', 'collection') # it's filter for exact match not for other so for that we defined filter class
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"] # provide by rest_framework for one or multiple keyword search in fields
    ordering_fields = ['unit_price', 'last_update'] # for sorting
    pagination_class = ProductPagination
    permission_classes = [IsAdminOrReadOnly]

    # Use this if you want to customize at ownotherwise use django-filter
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id') # use get method to avoid if id not given
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}

    # To change the logic for delete here we have to override destroy() method 
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': "Product can't be deleted due to it associated with order items."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product'))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': "Collection can't be deleted due to it associated with one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

class ReviewViewSet(ModelViewSet):
    # it will show the list of all for any selected product so for specific product all the reviews override get_querset
    # queryset = Review.objects.all() 
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']) 

    def get_serializer_context(self):
        # In kwargs we have product_pk and pk(review primary key)
        # we passing product_pk so on create the review we don't need to specify product
        # context passing use to pass data between views to serializer
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items', 'items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    # serializer_class = CartItemSerializer
    # list of methods we want to allow like except patch we want all other like this
    # also not it's should be in lower case
    http_method_names = ['get', 'post', 'put', 'delete'] 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PUT':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects \
                       .filter(cart_id=self.kwargs['cart_pk']) \
                       .select_related('product')

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # parser_classes = [FullDjangoModelPermission]
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()] # don't forget '()' 
    #     return [IsAuthenticated()]

    # To add a custom action use decoraters of rest_framework
    # Here if detail=False means it use listview ex: customers/me
    # Else if it's True then it use Detailview ex: customers/1/me
    # Here defined function name is added to endpoints end part as given above 'me' word
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # get_or_create method use to create if not exists. IT return tuple (instance, bool -> created or not)
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk=None):
        return Response('Ok')
    

class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
                        data=request.data, 
                        context={'user_id': self.request.user.id}
                    )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
