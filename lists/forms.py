from django import forms
from .models import *

#Here you can create your forms
class ProductForm(forms.ModelForm):
    name = models
    image = forms.ImageField(required=False)    

    class Meta:
        model = Product
        fields = ('product_name', 'brand', 'image')

        widgets = {
            'product_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'brand' : forms.TextInput(attrs={'class' : 'form-control'}),            
        }
    

class ProductWPriceForm(forms.ModelForm):
    name = models


    class Meta:
        model = ProductWPrice
        fields = ('product', 'price', 'amount', 'unit')

        widgets = {
            'product' : forms.Select(attrs={'class' : 'form-select'}),
            'price' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'unit' : forms.Select(attrs={'class' : 'form-select'}),

        }

class ListForm(forms.ModelForm):
    name = models

    class Meta:
        model = List
        fields = ('receipt_image', 'store', 'total')

        widgets = {
            'store' : forms.Select(attrs={'class' : 'form-select'}),
            'total' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '0.00'}),
        }

class StoreForm(forms.ModelForm):
    name = models
    image = forms.ImageField(required=False)

    class Meta:
        model = Store
        fields = ('name', 'location', 'image')

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Eg: H-E-B (Chipinque)'}),
            'location' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

class UnitForm(forms.ModelForm):
    name = models

    class Meta:
        model = Unit
        fields = ('unit', 'convert_to_int_sys')

        widgets = {
            'unit' : forms.TextInput(attrs={'class' : 'form-control'}),
            'convert_to_int_sys' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '0.00'}),
        }

class FilterProductDataForm(forms.Form):
    by_product_name = forms.BooleanField()
    by_brand = forms.BooleanField() 
    sort_by_cost = forms.BooleanField() 
    sort_by_unit_cost = forms.BooleanField()
    
    # class Meta:
    #     fields = ('by_product_name', 'by_brand', 'sort_by_cost', 'sort_by_unit_cost')

        # widgets = {
        #     'by_product_name' : forms.BooleanField(), 
        #     'by_brand' : forms.BooleanField(), 
        #     'sort_by_cost' : forms.BooleanField(), 
        #     'sort_by_unit_cost' : forms.BooleanField(),
        # }

