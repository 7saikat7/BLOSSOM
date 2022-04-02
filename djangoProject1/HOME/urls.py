
from PRODUCTR.views import view_cart
from django.urls import path ,include
from HOME import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    path('',views.home,name='home'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_signup/',views.user_create_account,name='user_signup'),
    path('user_logout/',views.user_logout,name='user_logout'),
#path('dashboard/',views.dashboard,name='dashboard'),
    path('activate_mail/<uid64>/<token>/',views.mail_activation,name='activate_mail'),
    path('contact_us/',views.contact_us,name='contact_us'),
    ###########          CRUD IN ADDRESS              #################
    
    path('add_address/',views.add_address,name='add_address'),
    #path('change_address/<int:pk>/',views.change_address,name='change_address'),
    path('delete_address/',views.delete_address,name='delete_address'),


    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)