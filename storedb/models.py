from django.db import models

# Create your models here.

class Product(models.Model):
    prod_name = models.CharField(max_length=30)
    prod_code = models.CharField(max_length=20)
   # prod_size = models.IntegerField()  # quantity
    prod_stock = models.IntegerField()
    #prod_unit = models.CharField(max_length=20)  # lt or kg
    prod_price = models.IntegerField()
    prod_reorder_level = models.IntegerField()

    def __str__(self):
        return self.prod_name


class Invoice(models.Model):
    cust_name = models.CharField(max_length=30)
    date = models.DateField()
    inv_no = models.CharField(max_length=15)
    prod_name = models.CharField(max_length=30)
   # prod_size = models.CharField(max_length=30)
   # prod_unit = models.CharField(max_length=10)
    prod_quant = models.IntegerField()
    prod_rate = models.IntegerField()
    total = models.IntegerField()
    discount = models.IntegerField(default=0)
    taxes = models.IntegerField(default=0)
    delivery = models.IntegerField(default=0)

    def __str__(self):
        return self.cust_name


class Inv_buff(models.Model):
    cust_name = models.CharField(max_length=30)
    date = models.DateField()
    inv_no = models.CharField(max_length=15)
    prod_name = models.CharField(max_length=30)
   # prod_size = models.CharField(max_length=30)
   # prod_unit = models.CharField(max_length=10)
    prod_quant = models.IntegerField()
    prod_rate = models.IntegerField()
    total = models.IntegerField()
    # discount = models.IntegerField(default=0)
    # taxes = models.IntegerField(default=0)
    # delivery = models.IntegerField(default=0)

    def __str__(self):
        return self.cust_name

class Order(models.Model):
    supp_name = models.CharField(max_length=30)
    date = models.DateField()
    order_no = models.CharField(max_length=20)
    prod_name = models.CharField(max_length=30)
  #  prod_size = models.CharField(max_length=30)
  #  prod_unit = models.CharField(max_length=10)
    prod_quant = models.IntegerField()
    prod_rate = models.IntegerField()
    total = models.IntegerField()
    discount = models.IntegerField(default=0)
    taxes = models.IntegerField(default=0)
    delivery = models.IntegerField(default=0)

    def __str__(self):
        return self.supp_name

class Order_buff(models.Model):
    supp_name = models.CharField(max_length=30)
    date = models.DateField()
    order_no = models.CharField(max_length=20)
    prod_name = models.CharField(max_length=30)
   # prod_size = models.CharField(max_length=30)
   # prod_unit = models.CharField(max_length=10)
    prod_quant = models.IntegerField()
    prod_rate = models.IntegerField()
    total = models.IntegerField()
    # discount = models.IntegerField(default=0)
    # taxes = models.IntegerField(default=0)
    # delivery = models.IntegerField(default=0)

    def __str__(self):
        return self.supp_name

class Transactions(models.Model):
    date = models.DateTimeField()
    prod_name = models.CharField(max_length=30)
    prod_quant = models.IntegerField()
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.prod_name

class Customer(models.Model):
    cust_name = models.CharField(max_length=20)
    inv_no = models.CharField(max_length=20)
    # copy from here
    ph1 = models.CharField(max_length= 14, default= "")
    ph2 = models.CharField(max_length=14, default= "")
    address = models.CharField(max_length=100, default= "")
    remarks = models.CharField(max_length=100, default= "")
    def __str__(self):
        return self.cust_name

class Supplier(models.Model):
    supp_name = models.CharField(max_length=20)
    order_no = models.CharField(max_length=20)
    ph1 = models.CharField(max_length=14, default="")
    ph2 = models.CharField(max_length=14, default="")
    address = models.CharField(max_length=100, default="")
    remarks = models.CharField(max_length=100, default="")
    def __str__(self):
        return self.supp_name