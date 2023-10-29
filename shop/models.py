from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=  models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name= models.CharField(max_length=200)
    price=  models.FloatField()
    digital=models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)
    image3 = models.ImageField(null=True,blank=True)
    image4 = models.ImageField(null=True,blank=True)
    category1 = models.CharField(max_length=200,null=True)
    category2 = models.CharField(max_length=200,null=True,blank=True)
    category3 = models.CharField(max_length=200,null=True,blank=True)
    color1= models.CharField(max_length=200,null=True,blank=True)
    color2= models.CharField(max_length=200,null=True,blank=True)
    color3= models.CharField(max_length=200,null=True,blank=True)
    color4= models.CharField(max_length=200,null=True,blank=True)    
    data=models.CharField(max_length=200,default='No description')
    #install pillow! and configure media root in settings!
    
    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                 null=True, blank=True) #user who ordered
    date_ordered= models.DateTimeField(auto_now_add=True) #the time of order
    complete = models.BooleanField(default=False) #is the order complete? 
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True

        return shipping


class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    color=models.CharField(max_length=200,null=True, blank=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    address= models.CharField(max_length=200)
    city= models.CharField(max_length=200)
    state= models.CharField(max_length=200)
    zipcode= models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    









                              






                                 
