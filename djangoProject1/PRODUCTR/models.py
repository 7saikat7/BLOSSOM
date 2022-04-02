from operator import mod
from pyexpat import model
import uuid
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.core.validators import MaxLengthValidator, MaxValueValidator,MinValueValidator
from django.db.models.fields.related import ForeignKey
from django.shortcuts import render
from django.utils.translation import deactivate
from django.utils import timezone



# Create your models here.
CHOICES=(

    ('plants','PLANTS'),
    ('Home_decore','CANDELS'),
    ('others','OTHERS'),
)
Sub_CAT_Choices=(

    ('indoor','INDOOR'),
    ('outdoor','OUTDOOR'),
    ('candels','CANDELS'),
    ('others','OTHER HOME DECORE'),

)
class Catagory(models.Model):
    Main_catagory=models.CharField(max_length=20 ,choices=CHOICES,default='plants')

    def __str__(self):
        return  str(self.Main_catagory)
class Sub_Catagory(models.Model):
    sub_Cat=models.ForeignKey(Catagory,on_delete=models.CASCADE,choices=Sub_CAT_Choices)

class Products(models.Model):
    """
    all required for palnts here !
    """
    Sub_catagory_p = models.ForeignKey(Catagory,on_delete=models.CASCADE,blank=False)
    custom_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=100)
    image1=models.ImageField(upload_to='plantimage/')
    image2 = models.ImageField(upload_to='plantimage/',blank=True,null=True)
    image3 = models.ImageField(upload_to='plantimage/',blank=True,null=True)
    description=models.TextField(max_length=1000)
    plant_type=models.CharField(max_length=100)
    max_price=models.PositiveIntegerField(default=1)
    off_price=models.PositiveIntegerField(default=1)
    quantity=models.PositiveIntegerField(default=1)
    height=models.PositiveIntegerField(default=1)
    width=models.PositiveIntegerField(default=1)
    light_type_for_plants_or_candels=models.CharField(max_length=100,default='low')
    fertilaizer=models.CharField(max_length=100,blank=True,null=True)
    watering_for_plant=models.CharField(max_length=100,blank=True,null=True)
    place_of_grown=models.CharField(max_length=100,blank=True,null=True)
    maintanance=models.CharField(max_length=1000,blank=True,null=True)
    special_features=models.CharField(max_length=50,blank=True,null=True)
    tips_plants =models.CharField(max_length=500,null=True,blank=True)
    shape_for_candels_others=models.CharField(max_length=100,default='',blank=True,null=True)
    material_for_candels_others=models.CharField(max_length=100,blank=True,null=True,default='')
   
    def __str__(self):
        return str(self.name) +'   prod_customid =  '+str(self.custom_id)


class Best_selling_product(models.Model):
    """
    Here will  be best selling products ! 

    """
    best_selling_product=models.ForeignKey(Products,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.best_selling_product)+" best - selling product"
###########################      ##########################################

                         #CART FEATURE 

##########################       ##########################################

class Cart(models.Model):
    auth_user= models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product_p=models.ForeignKey(Products,on_delete=models.CASCADE,blank=True)
    
    prod_quantity =models.PositiveIntegerField(default=1)
    toal_payable_amount=models.PositiveIntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return str(self.auth_user)+"'s   Cart"

class Coupon_code(models.Model):
 
   coupon_code_p =models.CharField(max_length=30,blank=True,null=True,unique=True)
   applied_to=models.ForeignKey(Products,on_delete=models.CASCADE,blank=True,null=True)
   valid_from =models.DateTimeField()
   valid_to =models.DateTimeField()
   discount=models.IntegerField(default=20)
   is_active=models.BooleanField(default=False)
    
   def __str__(self):
    return str(self.coupon_code_p)








################            adddress for user         ###############################
class Address(models.Model):
       user=models.ForeignKey(User,on_delete=models.CASCADE)
      
       f_add=models.CharField(max_length=1000,default='Full address')
       city_v=models.CharField(max_length=50,name='town')
       landmark=models.CharField(max_length=300,default='name')
       pin=models.CharField(max_length=8,default=71)
       ph_no=models.CharField(max_length=11,default=+91)
       alt_ph_no=models.CharField(max_length=11,default=+91,blank=True,null=True)
       def __str__(self):
           return str(self.f_add)+"  "+str(self.landmark)

######################    CHECKOUT AND PAYMENT ###############################

class Order(models.Model):
    Choices=(
        ("PLACED","PLACED"),
        ("SHIPPED","SHIPPED"),
        ("DELIVERED","DELIVERED"),
        ("CANCEL","CANCEL"),
    )
    customer_name=models.ForeignKey(User,on_delete=models.CASCADE)
    o_palced_name=models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    #o_palced_order_id=models.CharField(max_length=50,blank=True,null=True)
    date_time=models.DateField(default=timezone.now,auto_created=True)
    order_price=models.FloatField(default=1,null=True,blank=True)
    user_address=models.ForeignKey(Address,on_delete=models.CASCADE)
    order_quantity=models.IntegerField(default=1,blank=True,null=True)
    is_placed=models.BooleanField(default=False)
    placed=models.CharField(max_length=20,default='PLACED',choices=Choices)

    def __str__(self):
        return str(self.customer_name)+"'s order ---Paid="+str(self.is_placed)+"-----Current Status="+str(self.placed)






