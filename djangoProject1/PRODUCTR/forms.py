from django.forms import ModelForm
from .models import Address
from PRODUCTR import models
from django import forms

class Address_Form(forms.ModelForm):
   
   class Meta:
      model=Address
      fields='__all__'
      # excluse=('user')
