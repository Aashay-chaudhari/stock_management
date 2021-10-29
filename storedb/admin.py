from django.contrib import admin
from .models import Product,Inv_buff,Invoice, Order_buff, Order, Transactions, Customer, Supplier
# Register your models here.

admin.site.register(Product)

admin.site.register(Inv_buff)

admin.site.register(Invoice)

admin.site.register(Order_buff)

admin.site.register(Order)

admin.site.register(Transactions)

admin.site.register(Customer)

admin.site.register(Supplier)