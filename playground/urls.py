from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('cache_hello/', views.chache_hello),
    path('cache_cbv_hello/', views.chache_cbv_hello.as_view()),
]