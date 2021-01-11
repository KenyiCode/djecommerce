from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    # One User to one Customer, One Customer to one User
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    descrip = models.CharField(max_length=500, default="Write description...")
    
    # For items that are not physical products and don't need shipping
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    # Orders to Customer, One to Many
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    # For status of cart
    complete = models.BooleanField(default=False)

    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=False)

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    # One to Many with the product
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    # One to Many with Order (cart)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    # Attach to customer and order for redundancy
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address