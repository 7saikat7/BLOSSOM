from django.contrib import admin
from django.urls import path ,include

from .import views


app_name="PRODUCTR"

urlpatterns=[

 path('products/',views.all_products,name='all_products'),
 path('search/',views.search_p,name='search'),
 #path('search_c/',views.search_c,name='search_c'),
 #path('candle/',views.allcandels,name='allcandles'),
 path('products/<slug:pk>',views.all_products,name='detailprod_page'),
 #path('candle/<slug:pk_c>/',views.allcandels,name='detailprod_c_page'),
 #path('activate/',views.HOME.mail_activation,name='activate'),
 ###############            Cart urls            ##########################
 
 path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
 path('view_cart/',views.view_cart,name='view_cart'),
 path('plus_cart/',views.plus_cart,name='plus_cart'),
 path('buy_now_checkout/',views.buy_now_checkout,name='buy_now_checkout'),
 path('minus_cart/',views.minus_cart,name='minus_cart'),
 path('delete_cart/',views.remove_cart,name='delete_cart'),
 path('checkout/',views.checkout,name='checkout'),
 path('buy_now/',views.buy_now,name='buy_now'),
 path('payment_succes/',views.payment_succes,name='payment_succes'),
 path('dashboard/',views.dashboard,name='dashboard'),
 path('payment_done/',views.payment_done,name='payment_done'),
 path('payment_done_buynow/',views.payment_done_buynow,name='payment_done_buynow'),
 
 #path('buy_now',views.buy_now,name='buy_now'),
 #path('plant/add_to_cart/',views.bloom_add_cart),

]