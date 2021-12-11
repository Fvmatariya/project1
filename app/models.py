from django.db import models
from django.db.models.base import Model
from datetime import datetime


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20,default='user')
    pic = models.FileField(upload_to='profile pic',null=True,blank=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    cate = models.CharField(max_length=30,default='')
    des = models.TextField()
    price = models.CharField(max_length=20)
    pic = models.FileField(upload_to='products',null=True,blank=True)
#     quantity = models.IntegerField(default=1)


    def __str__(self):
        return self.uid.username + ' || ' + self.title 


class Cart(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=20,default='cart')
    amount = models.IntegerField(default=0)


    def __str__(self):
        return self.uid.email + self.product.title


        
class Buy(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount = models.IntegerField()
    quantity = models.IntegerField(default=1)
    pay_id = models.CharField(max_length=50)
    buy_date = models.DateTimeField(auto_now_add=True)
    expected_date = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=False)
    

    def __str__(self):
        return self.uid.email + ' ' + self.product.title
