from pprint import pprint
from django.urls import include, path
from . import views_fbv, views_api_cbv, views_generic_cbv, views_viewset_cbv
from rest_framework.routers import DefaultRouter 
# Below library give power to use nested routing - pip install drf-nested-routers
from rest_framework_nested import routers 

# router = DefaultRouter() # We can use SimpleRouter too but it' don't give urls endpoints and other benefits compare too this
router = routers.DefaultRouter() # for nesting routes we use this otherwise use above
router.register('products', views_viewset_cbv.ProductViewSet, basename='products') # we passed basename for to generte route name as per products-list, products-detail. Do this when not specify queryset attribute in viewset
router.register('collections', views_viewset_cbv.CollectionViewSet)
router.register('carts', views_viewset_cbv.CartViewSet)
router.register('customer', views_viewset_cbv.CustomerViewSet)
router.register('orders', views_viewset_cbv.OrderViewSet, basename='orders') # Have tospecify basename if queryset not defined instead have get_querset method then
# pprint(router.urls) # pprint for pretty printing
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views_viewset_cbv.ReviewViewSet, basename='product-reviews')
product_router.register('images', views_viewset_cbv.ProductImageViewSet, basename='product-images')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views_viewset_cbv.CartItemViewSet, basename='cart-items')

# urlpatterns = router.urls # one way to get urlpatterns for viewset views
# urlpatterns = router.urls + product_router.urls
urlpatterns = [
    # Function based views
    # path('products/', views_fbv.product_list),
    # path('products/<int:id>/', views_fbv.product_detail),
    # path('collections/', views_fbv.collection_list),
    # path('collections/<int:pk>/', views_fbv.collection_detail, name='collection-detail'), # for make hyperlink attribute should be pk not id or any.

    # Class based views
    # path('products/', views_api_cbv.ProductList.as_view()),
    # path('products/<int:id>/', views_api_cbv.ProductDetail.as_view()),
    # path('collections/', views_api_cbv.CollectionList.as_view()),
    # path('collections/<int:pk>/', views_api_cbv.CollectionDetail.as_view(), name='collection-detail'),

    # Class based with generic views
    # path('products/', views_generic_cbv.ProductList.as_view()),
    # path('products/<int:id>/', views_generic_cbv.ProductDetail.as_view()),
    # path('collections/', views_generic_cbv.CollectionList.as_view()),
    # path('collections/<int:pk>/', views_generic_cbv.CollectionDetail.as_view(), name='collection-detail'),

    # Class based with viewsets
    path('', include(router.urls)), # another way to define urls for viewset views, use it when want to define more urls otherwise use above
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)), 
]