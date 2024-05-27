from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
from uuid import uuid4
from .validators import validate_file_size


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # Here + in releted_name say that we don't want to make reverse relationship
    # in below attribute have to pass related_name due to collection already have back relation
    # with product having product_set so to remove this clash we either pass name or + not create relation
    featured_product = models.ForeignKey('Product', related_name='+', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    # Here defined null is for database to instruction that it can be null
    # For blank we specify to say django admin that for validation if it blank/null then not give error
    # specifying blank=True will remove blank validation error in add product of admin panel
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(1)]
        ) # max = 9999.99
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    # Here we define colletion first and then here we define relationship
    # What if it not defined first that class in that case inside the bracket use cotation for class name
    # example: colletion = models.ForeignKey('Colletion', on_delete=models.PROTECT)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # If we not defined related_name field option
    # then by default related_name will be product_set
    promotions = models.ManyToManyField(Promotion, blank=True)
    # If we defined related_name field option
    # then it will be use instead of product_set

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size])
    # image = models.FileField(upload_to='store/images', validators=[FileExtensionValidator(allowed_extensions=('pdf', 'docx'))])


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = (
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    )
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # class Meta:
    #     db_table = 'store_customers'
    #     indexes = [
    #         models.Index(fields=['first_name', 'last_name'])
    #     ]

    def __str__(self) -> str:
        # return f'{self.first_name} {self.last_name}'
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        # ordering = ['first_name', 'last_name']
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]
        


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETED, 'Completed'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    )
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order'),
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    # product = models.ForeignKey(Product, on_delete=models.PROTECT) # if you have this line use product.orderitem_set
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=6)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # For onetoone relationships
    # We make primary key to aviod django to create another table to make manytomany
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True) 
    # For manytomany relationships
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']] # have list of list due to have multiple groups(list) to be in one list for unique


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
