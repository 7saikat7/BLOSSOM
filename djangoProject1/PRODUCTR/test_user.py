from django.test import TestCase
import pytest
from django.contrib.auth.models import User
# from PRODUCTR.factory import UserFactory ,ProductFactory,CatagoryFactory
@pytest.mark.django_db
def test_new_faactoryuser(creating_user):
    #user=user_factory.build() # will create a user but wonn't save it to false database 
    print(creating_user)
    assert True

def test_product(product_factory):
    print("product testing is working ")
    product=product_factory.build()
    print(product.description)
    assert True

# @pytest.mark.django_db
# def test_check_password():
#     user_2=User.objects.create_user('saikat')
#     # user_2=User.objects.all()
#     user_2.set_password('omg')
#     #user1.set_password('password2222')
#     assert user_2.check_password('omg') is True
    
    

# def test_make_auser(user_a):
#     print(user_a.username)
#     print("-----")
#     print(user_a.is_staff)
#     assert user_a.username 






# @pytest.mark.django_db
# def test_create_user():
#     check =User.objects.create_user('saikat','saikat@saikat.com','test')
#     numbers=User.objects.all().count()
#     print(numbers)
#     assert User.objects.count() ==1
#     print(User.username)

# def test_check_user_exist():
#     check=User.objects.count()
#     try:
#         assert User.objects.count()==1
#         print('previous user exist..')
#     except:
#         assert User.objects.count()==0
#         print('There is no user avilable in database !')
