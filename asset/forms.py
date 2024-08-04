from django import forms
from .models import Item,Interest

class Itemform(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['EmpID', 'EmpName', 'Department', 'MobileNo', 'ProductName', 'ProductType','FinanceType', 'ProductDesc', 'ProductCount', 'ProductImage']

class Interestedform(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['EmpID', 'Department', 'MobileNo', 'Product_count']