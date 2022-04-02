from django.db.models.fields import CharField
from django.shortcuts import render ,redirect 
from django.contrib.auth.models import User,auth 
from django.contrib.auth import  login ,logout

from  django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from PRODUCTR.models import *
from django.urls import reverse
from django.contrib import messages
############# For E-mail ############
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from .signup_token import account_activation
from django.core.mail import EmailMessage, message
from django.contrib.sites.shortcuts import get_current_site


def home(request):
    B=Best_selling_product.objects.all()
    return render(request,'homepage.html',{'B':B})
def contact_us(request):
    return render(request,'contact_us.html')

def user_login(request):
    if request.method == 'POST':
        print("post request is working ")
        user_email = request.POST['username']
        user_password = request.POST['u_password']
        x = auth.authenticate(request, username=user_email, password=user_password)
        print('WE are getting a user')
        if x is not None:

            login(request, x)
            print("authenticated succesfull")
            return redirect('/')
        else:
            print("Not authenticating")
            contex2 = {'error4': "Invalid Username or Password"}
            return render(request, 'login.html', contex2)

    else:
        return render(request, 'login.html')

def user_logout(request):
   print('getting upto the url ')
   if request.method =='GET':
    print('Post request is working ')
    user=request.user
    logout(request)
    return redirect('/')
   else:
       print("no it's just a get request ")
       pass
def user_create_account(request):
    if request.method=='POST':
        email_fakeusername=request.POST['email_u']
        user_name=request.POST['user_name']
        ph_number=request.POST['ph_number']
        user_password=request.POST['type_password']
        re_type_password=request.POST['type_password_again']

        if user_password == re_type_password:
          try:
            new_user=User.objects.create_user(username=email_fakeusername,first_name=user_name,last_name=ph_number,password=user_password)
            new_user.is_active=False
            new_user.save()
            print('user saved succesfully in new account ')
            current_site = get_current_site(request)
            email_subject = "Blossoms Account Activation"
       
            message = render_to_string('account_activation.html', {
            
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                "token": account_activation.make_token(new_user),
            })
            print("generated tokens and encoded it ")
            to_email = request.POST['email_u']  # CHECK TO
            
            email = EmailMessage(email_subject, message, to=[to_email])
            print("got upto this ")
            email.send()
            print('email  has benn send to user ')
            contex = {'A': 'Please confirm your account activation mail and also check in sapm for mail'}
            # return redirect('/user_login/',foo='bara bara')bara
            return render(request,'verify_mail.html')
          except IntegrityError:
            return render(request, 'signup.html',
                          {'error2': "Email Is Already Taken, Try To login "})

        else:
            return render(request, 'signup.html',
                          {'error3': "Password Don't Match ! "})
            pass
    else:
        return render(request, 'signup.html')


def dashboard(request):
    user=request.user
    p=[i for i in Cart.objects.all() if user==user]

    return render(request,'dashboard.html',{'p':p})


def mail_activation(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and account_activation.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect("/user_login/")
    else:
        messages.warning(request,'Invalid Activation Link')
        return redirect("/contact_us/")


    
    

###########    Related to Address    ###############
     
def add_address(request):
  if request.method=='POST':
      
      f_add=request.POST['full_address']
      city_v=request.POST['city_v']
  
      land=request.POST['landmark']
      pin=request.POST['pin']
      ph_no=request.POST['1st_phone']
      alt_ph_no=request.POST['alt_phone_number']
      user=request.user
      p=Address(user=user,f_add=f_add,landmark=land,pin=pin,alt_ph_no=alt_ph_no,ph_no=ph_no).save()
      #return redirect(reverse('PRODUCTR:prod/view_cart/'))
      return redirect('PRODUCTR:view_cart')
  else:
    add=Address.objects.filter(user=request.user)
    contex={'add_all':add}
    return render(request,'update_address.html',contex)

def change_address(request,pk):
  
    pass
def delete_address(request):
    if request.method=='POST':
        id=request.POST['add_id']
        add=Address.objects.filter(pk=id)
        add.delete()
        return redirect('add_address')
    pass


