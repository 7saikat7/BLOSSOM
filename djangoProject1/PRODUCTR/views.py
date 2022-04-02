from ast import Add
from tkinter import E
from tokenize import PlainToken
from django.db.models.query_utils import Q
from django.forms import UUIDField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls.conf import path
from . models import *
from  django.contrib import auth, messages
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery , Q
from django.http import JsonResponse
from .forms import Address_Form
import razorpay
from django.core.paginator import Paginator ,EmptyPage
from django.core.mail import mail_admins ,send_mail
from django.http import HttpRequest
def all_products(request, pk=None):
    if pk:
        item=Products.objects.filter(pk=pk)
        #pagi=Paginator(item,20)

        return render(request,'detailprod_page.html',{'item':item})
    
    else:
     p=Products.objects.all()
     pagi=Paginator(p,2)
     pg=pagi.page(1)
        
     print(pagi)
     contex={'p':p,'info':'any info we need !'}
     return render(request,'allpant.html',contex)

def search_p(request):
   if request.method=='POST':
    query = request.POST['search_query']
    if query:
       print(query)
       if len(query) >= 100:
           search_results = []
           contex = {'search_results': search_results, 'query': query}
           return render(request, 'search.html', contex)
       else:
       
           print('......')
           search_results=Products.objects.annotate(search=SearchVector('name','description',)+SearchVector('plant_type','Sub_catagory_p',)+SearchVector('place_of_grown','maintanance','shape_for_candels_others','material_for_candels_others',)).filter(search=query)
           
   
           #search_results=Products.objects.filter(description__search=query)
           print(search_results)
           contex = {'search_results': search_results, 'query': query}
           return render(request, 'search.html', contex)
    else:
        return redirect('/')
   else:
       pass



##############     CART         ###############


def add_to_cart(request):
    
    if request.method == 'POST':
      print('Post request is working ')
      user=request.user
      if user.is_authenticated:
        searched_id=request.POST['prod_custom_id_cart']
        print(searched_id)
        A=Cart.objects.filter(Q(product_p=searched_id) & Q(auth_user=user))
        print(A)
        print('Alll--------')
        if A:
           return redirect('PRODUCTR:view_cart')
          
        else:
          print("Is this gonna work or not ")
          user_now=request.user
          prod_id=Products.objects.get(custom_id=searched_id) 
          print(prod_id)
          making_cart=Cart(auth_user=user_now,product_p=prod_id).save()
          print('product is saved to cart ')
              
          return redirect('PRODUCTR:view_cart')
        
      else:
        return redirect('user_login')
    else:
      print("get request is working not the post one !")
      pass
@login_required(login_url='/user_login/')
def view_cart(request):
  if request.method =='GET':
     user_current=request.user
     total_amount=0
     final_amount=0
     quantity=0
     
     #filter_cart=Cart.objects.filter(auth_user=user_current)
     #check_cart=[i for i in Cart.objects.all() if i.auth_user==user_current]
     check_cart=Cart.objects.filter(auth_user=user_current)
     if check_cart: 
       for p in check_cart:
        quantity +=p.prod_quantity
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
        total_amount+=temp_amount
        print('inside for loop so amount for each')
        print(total_amount) 

       p.toal_payable_amount=total_amount+50
       final_amount=total_amount+50
       add=Address.objects.filter(user=user_current)

       contex={'check_cart':check_cart,'total_amount':final_amount,'quantity':quantity,'no_object':'There is no object in the cart here !','add':add}
     
       return render(request,'show_cart.html',contex)

     return render (request,'show_cart.html',{'no_product':'No Product is found please go to product page !'})  
  else:
    try :  # not needed 
      user_current=request.user
      print(user_current)
      print('Got the user ----')
      add=Address_Form(request.POST,instance=user_current)
      if add.is_valid:
       print('add form data added ')
       jo=add.save(commit=False)
       jo.save()
       print('so saved all the data ')
       return redirect('view_cart')
      else:
        print("not valid")
        return redirect('view_cart',{'not_valid':'not_valid'})
      #p=Address(user=user,full_address=f_add,city_village=city_v,district=dist,landmark=land,pin=pin,alt_phone_number=alt_ph_no).save()
    except:
        return redirect('view_cart')

    
def plus_cart(request):
    if request.method =='GET':
     prod_id=request.GET['prod_id']
     user_current=request.user
     print(prod_id)
     print('prod id is taken for adding more items in cart ')
     check_cart=Cart.objects.get(Q(product_p=prod_id) & Q(auth_user=user_current))
     check_cart.prod_quantity +=1
     check_cart.save()
     
     total_amount=0
     final_amount=0
     quantity=0

     #check_cart=[i for i in Cart.objects.all() if i.auth_user==user_current]
     check_cart=Cart.objects.filter(auth_user=user_current)
     if check_cart:
       for p in check_cart:
        quantity +=p.prod_quantity
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
        total_amount+=temp_amount
        print('inside for loop of plus cart feature ')
        print(total_amount) 
       final_amount=total_amount+50
       plus_cart_res={
         'check_cart':quantity,
         'total_amount':final_amount}
       print('json response has been sent to ajax!')
       return JsonResponse(plus_cart_res)
     return render (request,'show_cart.html',{'no_product':'No Product is found please go to product page !'})    
    else:
      pass
def minus_cart(request):
 
  if request.method =='GET':
     prod_id=request.GET['prod_id']
     user_current=request.user
     print(prod_id)
     print('prod id is taken for adding more items in cart ')
     check_cart=Cart.objects.get(Q(product_p=prod_id) & Q(auth_user=user_current))
     check_cart.prod_quantity -=1
     if check_cart.prod_quantity <1 :
       check_cart.delete()
     else:
       check_cart.save()
     
     total_amount=0
     final_amount=0
     quantity=0

     check_cart=[i for i in Cart.objects.all() if i.auth_user==user_current]
     print(check_cart)
     if check_cart:
       for p in check_cart:
        quantity +=p.prod_quantity
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
        total_amount+=temp_amount
        print('inside for loop of plus cart feature ')
        print(total_amount) 
       final_amount=total_amount+50
       minus_cart_res={
         'check_cart':quantity,
         'total_amount':final_amount}
       print('json response has been sent to ajax!')
       return JsonResponse(minus_cart_res)
     return render (request,'show_cart.html',{'no_product':'No Product is found please go to product page !'})
  else:
      pass
def remove_cart(request):
  
  if request.method =='GET':
     prod_id=request.GET['prod_id']
     user_current=request.user
     print(prod_id)
     print('This is to remove the product from cart.... ')
     check_cart=Cart.objects.get(Q(product_p=prod_id) & Q(auth_user=user_current))
     check_cart.delete()
     
     total_amount=0
     final_amount=0
     quantity=0

     check_cart=[i for i in Cart.objects.all() if i.auth_user==user_current]
     print(check_cart)
     if check_cart:
       for p in check_cart:
        quantity +=p.prod_quantity
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
        total_amount+=temp_amount
        print('inside for loop of plus cart feature ')
        print(total_amount) 
       final_amount=total_amount+50
       delete_cart_res={
         'check_cart':quantity,
         'total_amount':final_amount}
       print('json response has been sent to ajax!')
       return JsonResponse(delete_cart_res)
     else:
       return render (request,'show_cart.html',{'no_product':'No Product is found please go to product page !'})

  else:
      pass

def buy_now(request):
  if request.method =='POST':
     user=request.user
     prod_id_buynow=request.POST['prod_custom_id']
     request.session['buy_NOW_prodid']=prod_id_buynow
     prod=Products.objects.filter(custom_id=prod_id_buynow)
     if prod:
      for i in prod:
       print('product already exists in buy now')
       product_id=i.custom_id
       print(product_id)
       prod_off=i.off_price
       prod_q=i.quantity
       prod_img=i.image1
       filter_add=Address.objects.filter(user=user)
       contex2={'p_id':product_id,'p_q':prod_q,'p_img':prod_img,'p':prod_off,'add':filter_add}
       #del request.session['buy_NOW_prodid']
      return render(request,'buy_now.html',contex2)
     pass
  else:
    pass

##################         PAYMENT     #########################
def checkout(request):
 if request.method =='POST':
  try:   
    add_id=request.POST['check_add_id'] 
    print(add_id)   
    request.session['addressid']=add_id
    # name = request.POST.get('name')

    # print("razor has done")
    if add_id:
      user=request.user
      print(add_id)
      filter_add=Address.objects.get(Q(pk=add_id) & Q(user=user))
      user_current=request.user
      total_amount=0
      final_amount=0
      quantity=0
      
      print("So it's the id of particular product we want wwwe are on  -------Checkout  ")
      #filter_cart=Cart.objects.filter(auth_user=user_current)
      check_cart=Cart.objects.filter(auth_user=user_current) 
      print(check_cart)
      
      if check_cart: 
        for p in check_cart:
            prod_id_verified=p.product_p.custom_id
            print("-------")
            print(prod_id_verified)
            #request.session['order_prod_id']=prod_id
            quantity +=p.prod_quantity
            temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
            total_amount+=temp_amount
          
            prod_name=p.product_p.custom_id
            print(prod_name)
            print(total_amount) 
            id_for_ordermodel=Products.objects.get(custom_id=prod_id_verified)
            print("prod id verified ....")
            p.toal_payable_amount=total_amount+50
            final_amount=total_amount+50
            request.session['FinalAmount']=final_amount
            request.session['Quantity']=quantity
            amount_in_paisa=final_amount*100
            
            print('order from checkout has been created')
            print(' So Mail has been sent to from checkout platform .... ')
           
            # print("so the raxor inmitiated for checkout only ")
            client = razorpay.Client(
            auth=('rzp_test_YxGmH9sme3dJFe','2RSePwFddZF9l9UIaTXbo7Gl'))
           
            payment = client.order.create({'amount': final_amount, 'currency': 'INR',
                                                'payment_capture': '1'})
            # Order(customer_name=user,o_palced_name=id_for_ordermodel,user_address=filter_add,order_price=final_amount,order_quantity=quantity).save()
            #cart.delete()
                    
        #  del request.session['order_prod_id']
        contex={'check_cart':check_cart,'T':total_amount,'total_amount':final_amount,'quantity':quantity,'filter_add':filter_add,'paisa':amount_in_paisa}
        #order_create=Order()

        return render(request,'checkout.html',contex)
        
    
    
      return render (request,'checkout.html',{'no_product':'Nothing to check out go for shopping !'})  
  
    else:
      return render (request,'checkout.html',{'no_add':'Nothing to check out go for shopping !'})  
  except Exception as e:
    print('except block is running ')
    print(e)
    return redirect('/add_address/')
 else:
    return redirect('/')
      
def payment_done(request):
  if request.method=='POST':
    user=request.user
    check_cart=Cart.objects.filter(auth_user=user)
    add_id=request.session.get('addressid')
    final_amount=request.session.get('FinalAmount')
    check_add=Address.objects.get(Q(pk=add_id) & Q(user=user))
    for p in check_cart:
     prod_id_verified=p.product_p.custom_id
     prod_name=p.product_p
     final_amount=request.session.get('FinalAmount')
     quantity=request.session.get('Quantity')
     Order(customer_name=user,o_palced_name=prod_name,user_address=check_add,order_price=final_amount,order_quantity=quantity).save()
     check_cart.delete()
    message=f"order has been created from {user}, amount paid ={final_amount}---- and Full address will be shown in database ==== {check_add}"
    send_mail(
                'New Order',
                 message,
                'foundationssaksham@gmail.com',
                ['jokesprogramming@gmail.com'],
                fail_silently=False,)
    print(' So Mail has been sent from payment done ... ')
    print("so the raxor inmitiated for payment done ")
    
    
    return redirect('PRODUCTR:dashboard')
  else:
    pass


def payment_done_buynow(request):
  if request.method=='POST':
    user=request.user
    p_id=request.session.get('buy_nowid')
    #p_id=uuid(p_id_for_decode)  # converting str to a UUID value to perform
    add_id=request.session.get('add_id')
    quantity=request.session.get('buy_quantity')
    final_price=request.session.get('final_price')
    Product_filter=Products.objects.filter(custom_id=p_id)
    print(Product_filter)
    
    for i in Product_filter:
      prod_name=i.name
      p=Products.objects.get(name=prod_name)
      print(prod_name)
      print(i.description)
      print(i.max_price)
      
      print("name of the product")
      add_chek=Address.objects.get(pk=add_id)
      Order.objects.create(customer_name=user,o_palced_name=p,user_address=add_chek,order_price=final_price,order_quantity=quantity).save()
    send_mail(
            'New Order',
            'New order created by user {{user}}, The product ID is {check_buy}  and The item will be delivered in {add_id}',
            'foundationssaksham@gmail.com',
            ['jokesprogramming@gmail.com'],
            fail_silently=False,)
    del request.session['buy_nowid']
    del request.session['add_id']
    del request.session['buy_quantity']
    del request.session['final_price']
    
    return redirect('PRODUCTR:dashboard')
  else:
    pass    

################        For Buy NOW CHECKOUT        ################
def buy_now_checkout(request):    
  if request.method =='POST':
    try:
      add_id=request.POST['check_add_id']
      desired_quantity=request.POST['desired_quality']
      #request.session['addressid']=add_id  
      print("razor has done for buy now products")
      if add_id:
        user=request.user
        print(add_id)
        filter_add_b=Address.objects.get(Q(pk=add_id) & Q(user=user))
        check_buy=request.session.get('buy_NOW_prodid')
        prod_buy=Products.objects.filter(custom_id=check_buy)
        for i in prod_buy:
          prod_b_id=i.custom_id
          #prod_pp=Products.objects.get(custom_id=prod_b_id)
          price=i.off_price*int(desired_quantity)
          final_price=price+50
          print(final_price)
          f_price_inpaisa=final_price*100
          print(f_price_inpaisa)
          #quantity_b=i.quantity
        
        client = razorpay.Client(
                auth=('rzp_test_YxGmH9sme3dJFe','2RSePwFddZF9l9UIaTXbo7Gl'))
        payment = client.order.create({'amount': final_price, 'currency': 'INR',
                                          'payment_capture': '1'})
                      
        # Order(customer_name=user,o_palced_name=prod_pp,user_address=filter_add_b,order_price=final_price,order_quantity=desired_quantity).save()
        #del request.session['buy_NOW_prodid']

        contex={'id':prod_b_id,'desired_quantity':desired_quantity,'price':final_price,'paisa':f_price_inpaisa,'prod':prod_buy,'add':filter_add_b}
       
        request.session['buy_nowid']=str(prod_b_id)  # converting a uuid field to str 
     
        request.session['buy_quantity']=desired_quantity
    
        request.session['add_id']=add_id
        request.session['final_price']=final_price
        return render(request,'checkout_2.html',contex)
    except Exception as E:
      print(E)
      return redirect('PRODUCTR:add_address')
def payment(request):  
     pass
  

@login_required(login_url='/user_login/')
def dashboard(request):
  user=request.user
  print("it's on dashboard ")
  address_id_check=request.session.get('addressid')  
  order_fetch = Order.objects.filter(customer_name=user)
  print(order_fetch)
  if order_fetch:
    for i in order_fetch:
     print(i.is_placed)
     print('New status of payment ..')
     i.is_placed=True
     i.save()
     mail_admins('New Order Placded by {user}'," New order has been created and paid by {user}",fail_silently=False, connection=None, html_message=None)
     #subject, message, fail_silently=False, connection=None, html_message=None
     
     print("so result new status is ")
     print(i.is_placed)
    contex={'O':order_fetch}
    return render(request,'dashboard.html',contex)
  return render(request,'dashboard.html',)

def payment_succes(request):
  pass
  
  #check_cart=[i for i in Cart.objects.all() if i.auth_user==user]

  #  current_user=request.user
  #  order=Cart.objects.filter(user=current_user)
  #  for i in 
  #  return render(request,'payment_succes.html')
     
     
