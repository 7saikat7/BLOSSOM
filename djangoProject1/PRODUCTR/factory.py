from django.contrib.auth import models
import factory
from faker import  Faker
from django.contrib.auth.models import User
from .models import Catagory,Products
fake=Faker()
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=User

    username=fake.name()
    is_staff='True'

class CatagoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Catagory
    Main_catagory='plants'

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Products
    
    sub_catagory_p='vvvvv'
    name=fake.name()
    uiid='a3c99176-31e8-4e69-87f3-122f2fe4022f'
    description=fake.text()
    plant_type='zugnu zugnu'
    max_price=324
    off_price=300
    
