import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from pytest_factoryboy import register
from PRODUCTR.factory import UserFactory ,ProductFactory,CatagoryFactory


register(UserFactory)  ### it will be used as user_factory   as per the doc 
register(ProductFactory)
register(CatagoryFactory)



@pytest.fixture
def creating_user(db,user_factory):
    #user=User.objects.create_user("test-user")
    user=user_factory.build()
    return user

# @pytest.fixture()
# def new_user_factory(db):   
#    def create_app(
#     username: str=None,
#     password: str=None,
#     first_name: str ="firstname",
#     last_name:str ="lastname",
#     email: str ="abc@gmail.com",
#     is_staff:str = False,
#     is_active: str =False,):

#     user=User.objects.create_user(
#       username=username,
#       password=password,
#       first_name=first_name,
#       last_name=last_name, 
#       email=email,
#       is_active=is_active,
#       is_staff=is_staff,)
#     return user
#    return create_app

# @pytest.fixture
# def user_a(db,new_user_factory):
#     return new_user_factory("Saikat go amr name","password","My name",is_staff="False")  