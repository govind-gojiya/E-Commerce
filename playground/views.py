from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Customer,Collection, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, Count, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Max, Min, Avg, Sum
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction
from django.db import connection

def say_hello(request):
    # x = 1
    # name = "govind"
    # return HttpResponse('Hello World')

    # ============ All ============
    # Get all the products
    # products = Product.objects.all()



    # ============ Get ============
    # Get only one product but it will give error if not found
    # try:
    #     # product = Product.objects.get(pk=1) # pk=id it select bsed on primary key
    #     product = Product.objects.get(pk=0)
    # except Product.DoesNotExist:
    #     print("No product found")
    # except ObjectDoesNotExist:
    #     print("Product not found")


    # Get only one product with filter
    #  it return none if not any
    # product = Product.objects.filter(id=0) # give none not error
    # if not product:
    #     print("No product found")



    # ============ Exists ============
    # Check product exists or not which give boolean result
    # is_product = Product.objects.filter(id=0).exists()
    # if not is_product:
    #     print("No product found")



    # ============ Filter ============
    # field lookup functions like:
    # exact, iexcat, gt, lt, gte, lte, range, in, isnull, contains, icontains, startswith, endswith, istartswith, iendswith
    # year, date, month, day, hour, minute, second, time, week, week_day
    # products = Product.objects.filter(title__icontains="coffee")
    # products = Product.objects.filter(description__isnull=True)
    # products = Product.objects.filter(unit_price__gt=20)
    # products = Product.objects.filter(unit_price__range=(20, 50))
    # products = Product.objects.filter(collection__id__in=[1, 2, 3, 4])


    # ============ Practice of filter ============
    # Question: Customers with .com accounts
    # customers = Customer.objects.filter(email__iendswith='.com')
    # return render(request, 'index.html', {'name': 'govind !', 'customers': list(customers)})

    # Question: Collections that don’t have a featured product
    # collections =  Collection.objects.filter(featured_product__isnull=True)

    # Question: Products with low inventory (less than 10)
    # products = Product.objects.filter(inventory__lt=10)

    # Question: Orders placed by customer with id = 1
    # orders = Order.objects.filter(customer__id=1)

    # Question: Order items for products in collection 3
    # order_items = OrderItem.objects.filter(product__collection__id=3)



    # ============ Q Object ============
    # It's short form of Query we can chain Q objects using bitwise operators Or(|), And(&)
    # products = Product.objects.filter(Q(inventory__gt=10) | ~Q(unit_price__lt=10)) # ~ negat sign menas not



    # ============ F function ============
    # If we want to compare value of one column with another column then we can use it
    # querset = Product.objects.filter(inventory=F('collection__id'))



    # ============ Ordering ============
    # For descending oder just add '-' sign 
    # products = Product.objects.order_by('unit_price', '-title') # Asc by unit_rice and desc by title
    # products = products.reverse() # It will reverse the order or rows
    
    # Both equal
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')

    # Both equal
    # product = Product.objects.order_by('unit_price')[-1]
    # product = Product.objects.latest('unit_price')



    # ============ Limiting ============
    # products = Product.objects.all()[:5] # product : 0, 1, 2, 3, 4 use only limit
    # products = Product.objects.all()[5:10] # product : 5, 6, 7, 8, 9 use limit and offset



    # ============ values and values_list ============
    # For select only defined columns
    # product = Product.objects.values('id', 'title', 'collection__title') # Give dictionary
    # Result [{'id': 1, 'title': 'Something', 'collection__title': 'Something'}, ...]
    # product = Product.objects.values_list('id', 'title', 'collection__title') # Give tuples
    # Result [(1, 'Something', 'something'), ...] 

    # ============ Practice ============
    # Question: Select a product which is placed and sort by product title
    # products = Product.objects.filter(id__in=OrderItem.objects.values_list('product_id').distinct()).order_by('title')



    # ============ only and defer ============
    # only is same as values just change is it return the same object
    # Note: Be careful if we access other attributes then specified in only or defer it will result in extra queries
    # In case of values it have dictionary so it will give none not make any queries
    # products = Product.objects.only('id', 'name')
    # In above products if we do products.unit_price result in extra queries

    # defer is opposite of only, in that we specify what to not select
    # products = Product.objects.defer('id', 'description')
    # It select all columns other than id and description but if we access that column it results in extra queries



    # ============ select_related and prefetch_related ============    
    # select_related use for one instention (1) - foreignkey or one-one rel - it make join in sql
    # prefetch_related use for many instention (n) - many-many rel - it make join in python
    # products = Product.objects.select_related('collection')
    # It make 1 join sql query and have product and respective colletion
    # products = Product.objects.prefetch_related('promotions').select_related('collection')
    # Here it will make 2 query, one for fetch product(with colletion info too) and second for select promotion as per product

    # Practice
    # Question: Get the last 5 orders with their customer and items (incl product)
    # orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]



    # ============ Aggregate ============
    # Return dictionary not querset object
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'), total=Sum('unit_price'))
    # return render(request, 'index.html', {'result': result})

    # Practice
    # Question: How many orders do we have?
    # result = Order.objects.aggregate(total_orders=Count('id')) # It give {'id__count': 1000} we can set key name as above
    # Question: How many units of product 1 have we sold?
    # result = OrderItem.objects.filter(product_id=1).aggregate(unit_sold=Sum('quantity'))
    # Question: How many orders has customer 1 placed?
    # result = Order.objects.filter(customer_id=1).aggregate(Count('id')) # or Order.objects.filter(customer_id=1).count()
    # Question: What is the min, max and average price of the products in collection 3?
    # result = Product.objects.filter(collection_id=3).aggregate(min=Min('unit_price'), max=Max('unit_price'), average=Avg('unit_price'))
    # return render(request, 'index.html', {'result': result})



    # ============ Annotation ============
    # To add a new field to each object we have annotate
    # Can be 4 types to assign new fields an expression:
        # 1. Value
        # 2. F
        # 3. Func
        # 4. Aggregate
        # 5. ExpressionWrapper

    # 1. Value
    # queryset = Customer.objects.annotate(new_field=Value(2)) # give any constant value like this, have to wrape around Value
    
    # 2. F
    # queryset = Customer.objects.annotate(new_id=F('id')+2) 
    
    # 3. Func
    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'), Value('_'), F('last_name'), function='CONCAT')
    #     )
    # Here defined function will be search from database function. So it's specific to database function
    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value('_'), 'last_name')
    # )
    # Here this will find sutable concate function for database and apply that one so better to use this if function is not specific to database function

    # 4. Aggregate
    # queryset = Customer.objects.annotate(order_count=Count('order'))

    # 5. ExpressionWrapper
    # Have to define output_field in this ExpressionsWrapper to make complex queries
    # discount_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price=discount_price)



    # ============ Filtering generic relational operators ============
    # contenttype = ContentType.objects.get_for_model(Product) 
    # this get_for_model only available for contenttype model not for other
    # taggeditems = TaggedItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type=contenttype,
    #         object_id=1
    #     )

    # If manager is defined method get_tags_for with above code to avoid repeation then
    # taggeditems = TaggedItem.objects.get_tags_for(Product, 1)










    # ============ Create ============
    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product(pk=1)
    # collection.save() # Best way to do by changing model attribute it change here to

    # or
    # collection = Collection.objects.create(title="Video Games", featured_product=None)



    # ============ Update ============
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = Product(pk=1)
    # collection.save() # It result in 2 query 
    # or
    # Collection.objects.filter(pk=11).update(title="Video Games") # Only 1 query done to update



    # ============ Delete ============
    # Collection.objects.filter(pk=11).delete()



    # ============ Atomic transcation ============
    # Here if order and orderitem created then and then only it commit in between failer result in rollback
    # with transaction.atomic():
    #     order = Order()
    #     order.customer = Customer(pk=1)
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product = Product(pk=1)
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()



    # ============ Raw query ============
    # on perticular model - return querset is different then our old queryset as like it 
    # queryset = Product.objects.raw("SELECT * FROM store_product")
    # to query on database
    # with connection.cursor() as cursor:
    #     cursor.execute("INSERT INTO store_collection (id, title, featured_product_id) VALUES(1, 'Video Games', null)")
        # for row in cursor.fetchall():
        #     print(row)
        # to call stored procedure
        # cursor.callproc('get_customer', [1, 2, 'a'])

    return render(request, 'index.html', {'name': 'govind !'})
