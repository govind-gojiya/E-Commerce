from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models
from django.db.models import Count, Value, CharField
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import TaggedItem
from django.db.models.functions import Concat


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory' # title shown in filter tab right side
    parameter_name = 'inventory' # shown in url parameter

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        # this function help to give list of custom filter in filter tab
        return [
            ('<10', 'Low'),
        ] # have to return list content value and human readable string

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory'] # actions we want to add to the dropdown list
    # fields = ['title', 'description'] # fields we want to show on add product page
    # exclude = ['promotions'] # exclude we want to not show on add product page
    # readonly_fields = ['promotions'] # readonly fields are only shown not editable on product page
    autocomplete_fields = ['collection'] 
    # autocomplete_fields for making searching for colltions but have to define search_fields list in listed item admin model
    prepopulated_fields = {
        'slug': ['title']
    } # to complete this as title field fill
    list_display = ('title', 'unit_price', 'inventory_status', 'collection_title')
    list_editable = ['unit_price']
    list_select_related = ['collection'] # If this is not set then it fire extra queries
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']

    def collection_title(self, product) -> str:
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product) -> str:
        if product.inventory < 10:
            return 'Low Stock'
        return 'Ok Stock'

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} product inventory successfully updated",
            messages.SUCCESS
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership', 'orders_count')
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    # search_fields = ['first_name', 'last_name'] # it's search with %query% we can add lookup as below
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = ( reverse('admin:store_order_changelist') 
               + '?'
               + urlencode({
                   'customer__id': customer.id
               }))
        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            orders_count=Concat(Count('order'), Value(' Orders'), output_field=CharField())
        )


class OrderItemInline(admin.TabularInline): 
    # also use admin.StackedInline it will show form in stack not in table form
    autocomplete_fields = ['product']
    min_num = 1 # minimum number of form to submit for parent to save
    max_num = 100 # maximum number of form can submit by parent to save
    model = models.OrderItem
    extra = 1 # By default it's 3 wecan set no of form we want to show


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ('id', 'placed_at', 'customer')
    inlines = [OrderItemInline] # use for specifying have to fill child form too for this


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # url = reverse('admin:app_model_page')
        url = (reverse('admin:store_product_changelist') 
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               }))
        return format_html("<a href={}>{}</a>", url, collection.products_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Concat(Count('product'), Value(' Product'), output_field=CharField())
        )

# admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)
