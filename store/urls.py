from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_list),
    path('products/<int:id>/', views.product_details),
]