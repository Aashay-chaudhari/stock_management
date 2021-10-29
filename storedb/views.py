from django.shortcuts import render, get_object_or_404
from .models import Product, Inv_buff, Invoice, Order_buff, Order, Transactions, Customer, Supplier
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from datetime import date


def delete_order(request,order_no):
    order_list2 = Order.objects.filter(order_no=order_no)
    for order in order_list2:
        prod_name = order.prod_name
        prod_quant = order.prod_quant
        prod = Product.objects.get(prod_name=prod_name)
        prod_stock_pre = prod.prod_stock
        prod.prod_stock = prod_stock_pre - prod_quant
        prod.save()
    Order.objects.filter(order_no=order_no).delete()
    return HttpResponseRedirect(reverse('home'))

def deleteinv(request,inv_no):
    inv_list2 = Invoice.objects.filter(inv_no=inv_no)
    for inv in inv_list2:
        prod_name = inv.prod_name
        prod_quant = inv.prod_quant
        prod = Product.objects.get(prod_name=prod_name)
        prod_stock_pre = prod.prod_stock
        prod.prod_stock = prod_stock_pre + prod_quant
        prod.save()
    Invoice.objects.filter(inv_no=inv_no).delete()
    return HttpResponseRedirect(reverse('home'))

def checkbox(request):
    prod_list = Product.objects.all()
    return render(request,'check.html',{'prod_list': prod_list})

#This is the source file
def supplier_list(request):
    return HttpResponseRedirect(reverse('show_supp'))

def customer_list(request):
    return HttpResponseRedirect(reverse('show_cust'))

def routeinv(request, inv_no):
    return HttpResponseRedirect(reverse('inv_details', args=[inv_no]))

def routeorder(request, order_no):
    return HttpResponseRedirect(reverse('order_details', args=[order_no]))

def cust_details(request, cust_name):
    inv_list = Invoice.objects.all().order_by('-id').filter(cust_name=cust_name)
    cust_name = cust_name
    return render(request, 'cust_details.html', {'inv_list': inv_list, 'cust_name': cust_name})

def supp_details(request,supp_name):
    order_list = Order.objects.all().order_by('-id').filter(supp_name=supp_name)
    supp_name= supp_name
    return render(request, 'supp_details.html', {'order_list':order_list,'supp_name': supp_name})

def show_cust(request):
    cust_list = Customer.objects.all()
    return render(request, 'showcust.html', {'cust_list':cust_list})


def show_supp(request):
    supp_list = Supplier.objects.all()

    return render(request, 'showsupp.html', {'supp_list':supp_list})


def show_prod(request):
    prod_list = Product.objects.all()
    return render(request, 'showprod.html', {'prod_list': prod_list})

def edit_cust(request, cust_id):
    id = cust_id
    cust = Customer.objects.get(pk=cust_id)
    cust_name = cust.cust_name
    inv_no = cust.inv_no
    ph1 = cust.ph1
    ph2 = cust.ph2
    address = cust.address
    remarks = cust.remarks

    context = {'cust_name': cust_name, 'inv_no': inv_no, 'ph1': ph1, 'ph2': ph2,
               'address': address, 'remarks': remarks, 'id': id}

    return render(request, 'edit_customer.html', context)

def edit_supp(request, supp_id):
    id = supp_id
    supp = Supplier.objects.get(pk=supp_id)
    supp_name = supp.supp_name
    order_no = supp.order_no
    ph1 = supp.ph1
    ph2 = supp.ph2
    address = supp.address
    remarks = supp.remarks

    context = {'supp_name':supp_name, 'order_no':order_no, 'ph1':ph1,'ph2':ph2,
               'address': address, 'remarks':remarks, 'id': id}

    return render(request, 'edit_supplier.html', context)


def edit_prod(request, prod_id):
    id = prod_id
    product = Product.objects.get(pk=prod_id)
    name = product.prod_name
    code = product.prod_code
    # size = product.prod_size
    # unit = product.prod_unit
    stock = product.prod_stock
    price = product.prod_price
    reorder = product.prod_reorder_level

    context = {'name': name, 'code': code,'stock': stock,
               'price': price, 'reorder': reorder, 'id': id}
    return render(request, 'edit_product.html', context)

def deletesupp(request, supp_name):
    order_list = Order.objects.order_by().values_list('supp_name', flat=True).distinct()
    text = "Unable to delete as Supplier is linked with existing orders."
    if supp_name in order_list:
        supp_list = Supplier.objects.all()
        return render(request, 'show_supp_error.html', {'text':text, 'supp_list':supp_list})

    else:
        Supplier.objects.filter(supp_name=supp_name).delete()
        return HttpResponseRedirect(reverse('home'))

def backtosupp(request):
    supp_list = Supplier.objects.all()
    return render(request, 'showsupp.html', {'supp_list': supp_list})


def deletecust(request, cust_name):
    inv_list = Invoice.objects.order_by().values_list('cust_name', flat=True).distinct()
    if cust_name in inv_list:
        cust_list = Customer.objects.all()
        return render(request, 'show_cust_error.html', {'cust_list': cust_list})

    else:
        Customer.objects.filter(cust_name=cust_name).delete()
        return HttpResponseRedirect(reverse('home'))


def updatecust(request):
    id = request.POST.get('id')
    cust = Customer.objects.get(pk=id)

    cust.cust_name = request.POST['name']
    cust.ph1 = request.POST['phone1']
    cust.ph2 = request.POST['phone2']
    cust.address = request.POST['address']
    cust.remarks = request.POST['remarks']
    cust.save()
    return HttpResponseRedirect('home')

def updatesupp(request):
    id = request.POST.get('id')
    supp = Supplier.objects.get(pk=id)

    supp.supp_name = request.POST['name']
    supp.ph1 = request.POST['phone1']
    supp.ph2 = request.POST['phone2']
    supp.address = request.POST['address']
    supp.remarks = request.POST['remarks']
    supp.save()
    return HttpResponseRedirect('home')


def updateproduct(request):
    id = request.POST.get('id')
    prod = Product.objects.get(pk=id)

    prod.prod_name = request.POST['prod_name']
    prod.prod_code = request.POST['code']
    #prod.prod_size = request.POST['size']  # quantity
    prod.prod_stock = request.POST['stock']
    #prod.prod_unit = request.POST['unit']
    prod.prod_price = request.POST['price']
    prod.prod_reorder_level = request.POST['reorder']
    prod.save()
    return HttpResponseRedirect(reverse('home'))


def deleteprod(request, prod_id):
    Product.objects.get(pk=prod_id).delete()
    return HttpResponseRedirect(reverse('home'))


def add_supplier(request):
    return render(request, 'add_supplier.html')


def add_customer(request):
    return render(request, 'add_customer.html')


def addsupp(request):
    supp_name = request.POST.get('name')
    supp_name = supp_name.title()

    supp_list = Supplier.objects.order_by().values_list('supp_name', flat=True).distinct()
    if supp_name in supp_list:
        return render(request, 'supp_exist.html', {'supp_name': supp_name})
    else:
        ph1 = request.POST.get('phone1')
        ph2 = request.POST.get('phone2')
        address = request.POST.get('address')
        remarks = request.POST.get('remark')
        Supplier.objects.create(supp_name=supp_name, ph1=ph1, ph2=ph2,
                                address=address, remarks=remarks)
        prod_list = Product.objects.all()
        return render(request, 'home.html', {'prod_list': prod_list})


def addcust(request):
    cust_name = request.POST.get('name')
    cust_name = cust_name.title()

    cust_list = Customer.objects.order_by().values_list('cust_name', flat=True).distinct()
    if cust_name in cust_list:
        return render(request, 'cust_exist.html', {'cust_name': cust_name})
    else:
        ph1 = request.POST.get('phone1')
        ph2 = request.POST.get('phone2')
        address = request.POST.get('address')
        remarks = request.POST.get('remark')
        Customer.objects.create(cust_name=cust_name, ph1=ph1, ph2=ph2,
                                address=address, remarks=remarks)
        prod_list = Product.objects.all()
        return render(request, 'home.html', {'prod_list': prod_list})


def home(request):
    prod_list = Product.objects.all()
    return render(request, 'home.html', {'prod_list': prod_list})

def addcustomer_inv(request):
    cust_name = request.POST['cust_name'].title()
    cust_list = Customer.objects.order_by().values_list('cust_name', flat=True).distinct()
    prod_list = Product.objects.all()
    today = date.today()
    if cust_name in cust_list:
        context = {
                        'prod_list': prod_list, 'today': today,
                        'cust_list': cust_list,
                        'cust_name': cust_name
                    }

        return render(request, 'cust_set_create_inv.html', context)
    else:
        Customer.objects.create(cust_name=cust_name, inv_no="0")
        prod_list = Product.objects.all()
        today = date.today()
        context = {
            'prod_list': prod_list, 'today': today,
            'cust_list': cust_list,
            'cust_name': cust_name
        }

        return render(request, 'cust_set_create_inv.html', context)



def create_invoice(request):
    prod_list = Product.objects.all()
    # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
    # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
    cust_list = Customer.objects.values('cust_name').distinct()
    today = date.today()
    cust_text = "Choose from existing customers"
    context = {
        'prod_list': prod_list, 'today': today,
        'cust_list': cust_list, 'cust_text': cust_text
    }

    return render(request, 'create_inv.html', context)




def inv_buff(request):
    if request.POST['action']=="addmore":
        inv_no = request.POST['invoice']
        inv_list = Invoice.objects.order_by().values_list('inv_no', flat=True).distinct()

        if inv_no in inv_list:
            text = "Duplicate Invoice Number"
            prod_list = Product.objects.all()
            # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
            # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
            cust_list = Customer.objects.values('cust_name').distinct()
            today = date.today()
            cust_text = "Choose from existing customers"
            context = {
                'prod_list': prod_list, 'today': today,
                'cust_list': cust_list, 'cust_text': cust_text, 'text': text
            }

            return render(request, 'create_inv.html', context)

        else:
            cust_name = request.POST['cust_name'].title()
            cust_list = Customer.objects.order_by().values_list('cust_name', flat=True).distinct()
            prod_list = Product.objects.all()
            today = date.today()
            if cust_name in cust_list:
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    inv_date = date.today()
                else:
                    inv_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])
                total = quantity * rate

                Inv_buff.objects.create(cust_name=request.POST['cust_name'],
                                        date=inv_date,
                                        inv_no=request.POST['invoice'],
                                        prod_name=request.POST['prod_name'],
                                        prod_quant=request.POST['quant'],
                                        prod_rate=request.POST['rate'],
                                        total=total)
                inv_buff_list = Inv_buff.objects.all()
                # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
                # prod_size_list = Product.objects.order_by().values('prod_size').distinct()

                context = {
                    'inv_buff_list': inv_buff_list, 'prod_list': prod_list,
                    'cust_name': inv_buff_list[0].cust_name, 'date': inv_buff_list[0].date,
                    'inv': inv_buff_list[0].inv_no
                }
                return render(request, 'create_inv_buff.html', context)
            else:
                Customer.objects.create(cust_name=cust_name, inv_no="0")
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    inv_date = date.today()
                else:
                    inv_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])
                total = quantity * rate

                Inv_buff.objects.create(cust_name=request.POST['cust_name'],
                                        date=inv_date,
                                        inv_no=request.POST['invoice'],
                                        prod_name=request.POST['prod_name'],
                                        prod_quant=request.POST['quant'],
                                        prod_rate=request.POST['rate'],
                                        total=total)
                inv_buff_list = Inv_buff.objects.all()
                # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
                # prod_size_list = Product.objects.order_by().values('prod_size').distinct()

                context = {
                    'inv_buff_list': inv_buff_list, 'prod_list': prod_list,
                    'cust_name': inv_buff_list[0].cust_name, 'date': inv_buff_list[0].date,
                    'inv': inv_buff_list[0].inv_no
                }
                return render(request, 'create_inv_buff.html', context)
    else:
        inv_no = request.POST['invoice']
        inv_list = Invoice.objects.order_by().values_list('inv_no', flat=True).distinct()

        if inv_no in inv_list:
            text = "Duplicate Invoice Number"
            prod_list = Product.objects.all()
            # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
            # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
            cust_list = Customer.objects.values('cust_name').distinct()
            today = date.today()
            cust_text = "Choose from existing customers"
            inv_buff_list = Inv_buff.objects.all()
            context = {
                'inv_buff_list': inv_buff_list,'prod_list': prod_list, 'today': today,
                'cust_list': cust_list, 'cust_text': cust_text, 'text': text
            }

            return render(request, 'create_inv.html', context)

        else:
            cust_name = request.POST['cust_name'].title()
            cust_list = Customer.objects.order_by().values_list('cust_name', flat=True).distinct()
            prod_list = Product.objects.all()
            today = date.today()
            if cust_name in cust_list:
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    inv_date = date.today()
                else:
                    inv_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])
                total = quantity * rate

                Inv_buff.objects.create(cust_name=request.POST['cust_name'],
                                        date=inv_date,
                                        inv_no=request.POST['invoice'],
                                        prod_name=request.POST['prod_name'],
                                        prod_quant=request.POST['quant'],
                                        prod_rate=request.POST['rate'],
                                        total=total)
                inv_buff_list = Inv_buff.objects.all()
                # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
                # prod_size_list = Product.objects.order_by().values('prod_size').distinct()

                context = {
                    'inv_buff_list': inv_buff_list, 'prod_list': prod_list,
                    'cust_name': inv_buff_list[0].cust_name, 'date': inv_buff_list[0].date,
                    'inv': inv_buff_list[0].inv_no
                }
                return render(request, 'cust_set_create_inv.html', context)
            else:
                Customer.objects.create(cust_name=cust_name, inv_no="0")
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    inv_date = date.today()
                else:
                    inv_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])
                total = quantity * rate

                Inv_buff.objects.create(cust_name=request.POST['cust_name'],
                                        date=inv_date,
                                        inv_no=request.POST['invoice'],
                                        prod_name=request.POST['prod_name'],
                                        prod_quant=request.POST['quant'],
                                        prod_rate=request.POST['rate'],
                                        total=total)
                inv_buff_list = Inv_buff.objects.all()
                # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
                # prod_size_list = Product.objects.order_by().values('prod_size').distinct()

                context = {
                    'inv_buff_list': inv_buff_list, 'prod_list': prod_list,
                    'cust_name': inv_buff_list[0].cust_name, 'date': inv_buff_list[0].date,
                    'inv': inv_buff_list[0].inv_no
                }
                return render(request, 'cust_set_create_inv.html', context)





def inv_addmore(request):
    if request.POST['action']=="addmore":
        prod_list = Product.objects.all()

        inv_buff_list = Inv_buff.objects.all()
        cust_name = inv_buff_list[0].cust_name
        date = inv_buff_list[0].date
        inv = inv_buff_list[0].inv_no

        # size = int(request.POST['size'])
        quantity = int(request.POST['quant'])
        rate = int(request.POST['rate'])

        total = quantity * rate

        Inv_buff.objects.create(cust_name=cust_name,
                                date=date,
                                inv_no=inv,
                                prod_name=request.POST['prod_name'],
                                prod_quant=request.POST['quant'],
                                prod_rate=request.POST['rate'],
                                total=total
                                )
        #
        # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
        # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
        context = {'inv_buff_list': inv_buff_list, 'prod_list': prod_list,
                   'cust_name': cust_name, 'date': date, 'inv': inv,
                   'total': total}
        return render(request, 'create_inv_buff.html', context)
    else:
        prod_list = Product.objects.all()

        inv_buff_list = Inv_buff.objects.all()
        cust_name = inv_buff_list[0].cust_name
        date = inv_buff_list[0].date
        inv = inv_buff_list[0].inv_no

        # size = int(request.POST['size'])
        quantity = int(request.POST['quant'])
        rate = int(request.POST['rate'])

        total = quantity * rate

        Inv_buff.objects.create(cust_name=cust_name,
                                date=date,
                                inv_no=inv,
                                prod_name=request.POST['prod_name'],
                                prod_quant=request.POST['quant'],
                                prod_rate=request.POST['rate'],
                                total=total
                                )
        #
        # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
        # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
        context = {'inv_buff_list': inv_buff_list, 'prod_list': prod_list,
                   'cust_name': cust_name, 'date': date, 'inv': inv,
                   'total': total}
        return render(request, 'cust_set_create_inv.html', context)




def insertInv(request):
    prod_list = Product.objects.all()
    inv_buff_list = Inv_buff.objects.all()
    discount = int(request.POST['disc'])
    taxes = int(request.POST['tax'])
    delivery = int(request.POST['delivery'])
    for c in inv_buff_list:
        prod = get_object_or_404(Product, prod_name=c.prod_name)

        prod.prod_stock = prod.prod_stock - c.prod_quant
        prod.save()

        invoice = Invoice.objects.create(cust_name=c.cust_name,
                                         date=c.date,
                                         inv_no=c.inv_no,
                                         prod_name=c.prod_name,
                                         prod_quant=c.prod_quant,
                                         prod_rate=c.prod_rate,
                                         total=c.total,
                                         discount=discount,
                                         taxes=taxes,
                                         delivery=delivery)
        transaction = Transactions.objects.create(date=c.date,
                                                  prod_name=c.prod_name,
                                                  prod_quant=c.prod_quant,
                                                  name='Sale',
                                                  number=c.inv_no)
    Inv_buff.objects.all().delete()

    return HttpResponseRedirect(reverse('home'))


def inv_list(request):
    # invoice = Invoice.objects.order_by('-id').distinct()
    inv_list1 = Invoice.objects.order_by().values_list('date','inv_no','cust_name').distinct()
    # return HttpResponse(inv_list)
    print(inv_list1)
    return render(request, 'invoiceList.html', {'inv_list': inv_list1})


def toinvlists(request):
    return HttpResponseRedirect(reverse('inv_list'))


def inv_details(request, inv_no):

    inv = Invoice.objects.all().filter(inv_no=inv_no)
    inv_cust_name = inv[0].cust_name
    inv_date = inv[0].date
    inv_total = inv[0].total
    inv_no = inv[0].inv_no
    total = 0
    discount = inv[0].discount
    tax = inv[0].taxes
    delivery = inv[0].delivery
    for i in inv:
        total = i.total + total
    final_total = total-discount+tax+delivery
    context = {'inv': inv, 'inv_cust_name': inv_cust_name,
               'inv_date': inv_date, 'inv_total': inv_total,
               'inv_no': inv_no, 'total': final_total, 'discount':discount,
               'tax':tax, 'delivery':delivery}
    return render(request, 'inv_details.html', context)


def edit_inv(request, inv_no):
    inv = Invoice.objects.all().filter(inv_no=inv_no)
    inv_cust_name = inv[0].cust_name
    inv_date = inv[0].date
    inv_total = inv[0].total
    inv_no = inv[0].inv_no
    discount = inv[0].discount
    tax = inv[0].taxes
    delivery = inv[0].delivery
    total = 0
    for i in inv:
        total = i.total + total
    final_total = total - discount + tax + delivery
    context = {'inv': inv, 'inv_cust_name': inv_cust_name,
               'inv_date': inv_date, 'inv_total': inv_total, 'inv_no': inv_no,
               'total': final_total, 'discount':discount,
               'tax':tax, 'delivery':delivery}
    return render(request, 'edit_inv.html', context)

def update_order_disc(request, order_no, order_upd_no):
    orders = Order.objects.all().filter(order_no=order_no)
    discount = request.POST['discount']
    taxes = request.POST['taxes']
    delivery = request.POST['delivery']
    discount = int(discount)
    taxes = int(taxes)
    delivery = int(delivery)
    for i in orders:
        i.discount = discount
        i.taxes = taxes
        i.delivery = delivery
        i.save()
    return HttpResponseRedirect(reverse('edit_order', args=[order_no]))

def update_inv_disc(request, inv_no, inv_upd_no):
    invoices = Invoice.objects.all().filter(inv_no=inv_no)
    discount = request.POST['discount']
    taxes = request.POST['taxes']
    delivery = request.POST['delivery']
    discount = int(discount)
    taxes = int(taxes)
    delivery = int(delivery)
    for i in invoices:
        i.discount = discount
        i.taxes = taxes
        i.delivery = delivery
        i.save()
    return HttpResponseRedirect(reverse('edit_inv', args=[inv_no]))



def update_inv(request, inv_no, inv_upd_no):
    inv = get_object_or_404(Invoice, pk=inv_upd_no)

    prod_name = request.POST['prod_name']

    prod1 = get_object_or_404(Product, prod_name=prod_name)

    stock = prod1.prod_stock
    earlier_quant = inv.prod_quant
    new_quant = int(request.POST['quant'])
    result = stock + earlier_quant - new_quant
    prod1.prod_stock = result
    prod1.save()

    prod_quant = request.POST['quant']
    prod_rate = request.POST['rate']
    inv = Invoice.objects.get(pk=inv_upd_no)
    inv.prod_quant = prod_quant
    inv.prod_rate = prod_rate

    inv.total = int(inv.prod_quant) * int(inv.prod_rate)
    inv.save()

    inv1 = Invoice.objects.all().filter(inv_no=inv_no)
    inv_cust_name = inv.cust_name
    inv_date = inv.date
    inv_total = inv.total
    inv_no = inv.inv_no
    total = 0
    context = {'inv': inv, 'inv_cust_name': inv_cust_name,
               'inv_date': inv_date, 'inv_total': inv_total, 'inv_no': inv_no,
               'total': total}

    return HttpResponseRedirect(reverse('edit_inv', args=[inv_no]))


def save_inv(request, inv_no):
    return HttpResponseRedirect(reverse('inv_list'))


def printinv(request, inv_no):
    inv = Invoice.objects.all().filter(inv_no=inv_no)
    inv_cust_name = inv[0].cust_name
    inv_date = inv[0].date
    inv_total = inv[0].total
    inv_no = inv[0].inv_no
    total = 0
    for i in inv:
        total = i.total + total
    context = {'inv': inv, 'inv_cust_name': inv_cust_name,
               'inv_date': inv_date, 'inv_total': inv_total,
               'inv_no': inv_no, 'total': total}
    return render(request, 'print_inv.html', context)


def print_inv_list(request):
    invoice = Invoice.objects.order_by().values('date', 'inv_no', 'cust_name').distinct()
    # I will resume work on this page after i fix the unique constraints using javascript. if i want
    # to make sure input is unique, i can pass a list, and vrify against that list in javascript if element is there or not

    return HttpResponse(invoice)


def print_order_list(request):
    pass;


def printorder(request, inv_no):
    order = Order.objects.all().filter(order_no=order_no)
    order_supp_name = order[0].supp_name
    order_date = order[0].date
    order_total = order[0].total
    order_no = order[0].order_no
    total = 0
    for i in order:
        total = i.total + total
    context = {'order': order, 'order_supp_name': order_supp_name,
               'order_date': order_date, 'order_total': order_total,
               'order_no': order_no, 'total': total}
    return render(request, 'print_order.html', context)


def cancel(request):
    Inv_buff.objects.all().delete()
    Order_buff.objects.all().delete()
    return HttpResponseRedirect(reverse('home'))


def addproduct(request):
    return render(request, 'addproduct.html')


def insertprod(request):
    prod_name = request.POST.get('prod_name')
    prod_list = Product.objects.order_by().values_list('prod_name', flat=True).distinct()
    prod_name = prod_name.title()
    if prod_name in prod_list:
        message = "Product already exists."
        return render(request, 'addproduct.html', {'message': message})
    else:
        prod_code = request.POST['code']
       # prod_size = request.POST['size']  # quantity
        prod_stock = request.POST['stock']
       # prod_unit = request.POST['unit']
        prod_price = request.POST['price']
        prod_reorder_level = request.POST['reorder']
        Product.objects.create(prod_name=prod_name, prod_code=prod_code,
                                prod_stock=prod_stock,
                               prod_price=prod_price,
                               prod_reorder_level=prod_reorder_level)

        return HttpResponseRedirect(reverse('home'))


def show_details_inv(request, inv_no):
    return HttpResponseRedirect(reverse('inv_details', args=[inv_no]))


def show_details_order(request, order_no):
    return HttpResponseRedirect(reverse('order_details', args=[order_no]))


def product_trans(request, prod_name):
    prod_trans_list = Transactions.objects.order_by('-id').filter(prod_name=prod_name)
    return render(request, 'prod_trans_list.html', {'prod_trans_list': prod_trans_list})


def show_transactions(request):
    trans_list = Transactions.objects.order_by().values_list('date', 'number', 'name').distinct()
    return render(request, 'trans_list.html', {'trans_list': trans_list})


def create_order(request):
    prod_list = Product.objects.all()
    # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
    # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
    supp_list = Supplier.objects.values('supp_name').distinct()
    today = date.today()
    supp_text = "Choose from existing suppliers"
    context = {
        'prod_list': prod_list, 'today': today,
        'supp_list': supp_list, 'supp_text': supp_text
    }
    return render(request, 'create_order.html', context)


def addsupplier_order(request):
    supp_name = request.POST['supp_name'].title()
    supp_list = Supplier.objects.order_by().values_list('supp_name', flat=True).distinct()
    prod_list = Product.objects.all()
    today = date.today()
    if supp_name in supp_list:
        context = {
                        'prod_list': prod_list, 'today': today,
                        'supp_list': supp_list,
                        'supp_name': supp_name
                    }

        return render(request, 'supp_set_create_order.html', context)
    else:
        Supplier.objects.create(supp_name=supp_name, order_no="0")
        prod_list = Product.objects.all()
        today = date.today()
        context = {
            'prod_list': prod_list, 'today': today,
            'supp_list': supp_list,
            'supp_name': supp_name
        }

        return render(request, 'supp_set_create_order.html', context)


def order_buff(request):
    if request.POST['action']=="addmore":
        order_no = request.POST['order']
        order_list = Order.objects.order_by().values_list('order_no', flat=True).distinct()

        if order_no in order_list:
            text = "Duplicate Order Number"
            prod_list = Product.objects.all()
            # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
            # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
            order_list = Order.objects.values('order_no').distinct()
            today = date.today()
            context = {
                'prod_list': prod_list, 'today': today,
                'order_list': order_list, 'text': text
            }

            return render(request, 'create_order.html', context)

        else:
            supp_name = request.POST['supp_name'].title()
            supp_list = Supplier.objects.order_by().values_list('supp_name', flat=True).distinct()
            prod_list = Product.objects.all()
            today = date.today()
            if supp_name in supp_list:
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    order_date = date.today()
                else:
                    order_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])

                total = quantity * rate

                Order_buff.objects.create(supp_name=request.POST['supp_name'],
                                          date=order_date,
                                          order_no=request.POST['order'],
                                          prod_name=request.POST['prod_name'],
                                          prod_quant=request.POST['quant'],
                                          prod_rate=request.POST['rate'],
                                          total=total
                                          )
                order_buff_list = Order_buff.objects.all()

                context = {
                    'order_buff_list': order_buff_list, 'prod_list': prod_list,
                    'supp_name': order_buff_list[0].supp_name, 'date': order_buff_list[0].date,
                    'order_no': order_buff_list[0].order_no, 'total': total}
                return render(request, 'create_order_buff.html', context)
            else:
                Supplier.objects.create(supp_name=supp_name, order_no="0")
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    order_date = date.today()
                else:
                    order_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])

                total = quantity * rate

                Order_buff.objects.create(supp_name=request.POST['supp_name'],
                                          date=order_date,
                                          order_no=request.POST['order'],
                                          prod_name=request.POST['prod_name'],
                                          prod_quant=request.POST['quant'],
                                          prod_rate=request.POST['rate'],
                                          total=total
                                          )
                order_buff_list = Order_buff.objects.all()

                context = {
                    'order_buff_list': order_buff_list, 'prod_list': prod_list,
                    'supp_name': order_buff_list[0].supp_name, 'date': order_buff_list[0].date,
                    'order_no': order_buff_list[0].order_no, 'total': total}
                return render(request, 'create_order_buff.html', context)
    else:
        order_no = request.POST['order']
        order_list = Order.objects.order_by().values_list('order_no', flat=True).distinct()

        if order_no in order_list:
            text = "Duplicate Order Number"
            prod_list = Product.objects.all()
            # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
            # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
            order_list = Order.objects.values('order_no').distinct()
            today = date.today()
            context = {
                'prod_list': prod_list, 'today': today,
                'order_list': order_list, 'text': text
            }

            return render(request, 'create_order.html', context)

        else:
            supp_name = request.POST['supp_name'].title()
            supp_list = Supplier.objects.order_by().values_list('supp_name', flat=True).distinct()
            prod_list = Product.objects.all()
            today = date.today()
            if supp_name in supp_list:
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    order_date = date.today()
                else:
                    order_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])

                total = quantity * rate

                Order_buff.objects.create(supp_name=request.POST['supp_name'],
                                          date=order_date,
                                          order_no=request.POST['order'],
                                          prod_name=request.POST['prod_name'],
                                          prod_quant=request.POST['quant'],
                                          prod_rate=request.POST['rate'],
                                          total=total
                                          )
                order_buff_list = Order_buff.objects.all()

                context = {
                    'order_buff_list': order_buff_list, 'prod_list': prod_list,
                    'supp_name': order_buff_list[0].supp_name, 'date': order_buff_list[0].date,
                    'order_no': order_buff_list[0].order_no, 'total': total}
                return render(request, 'supp_set_create_order.html', context)
            else:
                Supplier.objects.create(supp_name=supp_name, order_no="0")
                prod_list = Product.objects.all()
                if (request.POST['start_date'] == ''):
                    order_date = date.today()
                else:
                    order_date = request.POST['start_date']

                # size = int(request.POST['size'])
                quantity = int(request.POST['quant'])
                rate = int(request.POST['rate'])

                total = quantity * rate

                Order_buff.objects.create(supp_name=request.POST['supp_name'],
                                          date=order_date,
                                          order_no=request.POST['order'],
                                          prod_name=request.POST['prod_name'],
                                          prod_quant=request.POST['quant'],
                                          prod_rate=request.POST['rate'],
                                          total=total
                                          )
                order_buff_list = Order_buff.objects.all()

                context = {
                    'order_buff_list': order_buff_list, 'prod_list': prod_list,
                    'supp_name': order_buff_list[0].supp_name, 'date': order_buff_list[0].date,
                    'order_no': order_buff_list[0].order_no, 'total': total}
                return render(request, 'supp_set_create_order.html', context)




def order_addmore(request):
    if request.POST['action']=="addmore":
        prod_list = Product.objects.all()

        order_buff_list = Order_buff.objects.all()
        supp_name = order_buff_list[0].supp_name
        date = order_buff_list[0].date
        order = order_buff_list[0].order_no

        # size = int(request.POST['size'])
        quantity = int(request.POST['quant'])
        rate = int(request.POST['rate'])

        total = quantity * rate

        Order_buff.objects.create(supp_name=supp_name,
                                date=date,
                                order_no=order,
                                prod_name=request.POST['prod_name'],
                                prod_quant=request.POST['quant'],
                                prod_rate=request.POST['rate'],
                                total=total
                                )
        #
        # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
        # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
        context = {'order_buff_list': order_buff_list, 'prod_list': prod_list,
                   'supp_name': supp_name, 'date': date, 'order': order,
                   'total': total}
        return render(request, 'create_order_buff.html', context)
    else:
        prod_list = Product.objects.all()

        order_buff_list = Order_buff.objects.all()
        supp_name = order_buff_list[0].supp_name
        date = order_buff_list[0].date
        order = order_buff_list[0].order_no

        # size = int(request.POST['size'])
        quantity = int(request.POST['quant'])
        rate = int(request.POST['rate'])

        total = quantity * rate

        Order_buff.objects.create(supp_name=supp_name,
                                date=date,
                                order_no=order,
                                prod_name=request.POST['prod_name'],
                                prod_quant=request.POST['quant'],
                                prod_rate=request.POST['rate'],
                                total=total
                                )
        #
        # prod_unit_list = Product.objects.order_by().values('prod_unit').distinct()
        # prod_size_list = Product.objects.order_by().values('prod_size').distinct()
        context = {'order_buff_list': order_buff_list, 'prod_list': prod_list,
                   'supp_name': supp_name, 'date': date, 'order': order,
                   'total': total}
        return render(request, 'supp_set_create_order.html', context)


def insertOrder(request):
    prod_list = Product.objects.all()
    order_buff_list = Order_buff.objects.all()
    discount = int(request.POST['disc'])
    taxes = int(request.POST['tax'])
    delivery = int(request.POST['delivery'])

    for c in order_buff_list:
        prod = get_object_or_404(Product, prod_name=c.prod_name)

        prod.prod_stock = prod.prod_stock + c.prod_quant
        prod.save()
        Order.objects.create(supp_name=c.supp_name,
                             date=c.date,
                             order_no=c.order_no,
                             prod_name=c.prod_name,
                             prod_quant=c.prod_quant,
                             prod_rate=c.prod_rate,
                             total=c.total,
                             discount=discount,
                             taxes=taxes,
                             delivery=delivery
                             )
        transaction = Transactions.objects.create(date=c.date,
                                                  prod_name=c.prod_name,
                                                  prod_quant=c.prod_quant,
                                                  name='Purchase',
                                                  number=c.order_no)
    Order_buff.objects.all().delete()

    return HttpResponseRedirect(reverse('home'))


def order_list(request):
    order2 = Order.objects.order_by().values_list('date', 'order_no', 'supp_name').distinct()
    print(order2)
    return render(request, 'orderList.html', {'order': order2})


def order_details(request, order_no):
    order = Order.objects.all().filter(order_no=order_no)
    order_supp_name = order[0].supp_name
    order_date = order[0].date
    order_total = order[0].total
    order_no = order[0].order_no
    discount = order[0].discount
    tax = order[0].taxes
    delivery = order[0].delivery
    total = 0
    for i in order:
        total = i.total + total
    final_total = total - discount + tax + delivery
    context = {'order': order, 'order_supp_name': order_supp_name,
               'order_date': order_date, 'order_total': order_total,
               'order_no': order_no, 'total': final_total, 'discount':discount,
               'tax':tax, 'delivery':delivery}
    return render(request, 'order_details.html', context)


def toorderlists(request):
    return HttpResponseRedirect(reverse('order_list'))


def edit_order(request, order_no):
    order = Order.objects.all().filter(order_no=order_no)
    order_supp_name = order[0].supp_name
    order_date = order[0].date
    order_total = order[0].total
    order_no = order[0].order_no
    discount = order[0].discount
    tax = order[0].taxes
    delivery = order[0].delivery
    total = 0
    for i in order:
        total = i.total + total
    final_total = total - discount + tax + delivery
    context = {'order': order, 'order_supp_name': order_supp_name,
               'order_date': order_date, 'order_total': order_total, 'order_no': order_no,
               'total': final_total, 'discount':discount,
               'tax':tax, 'delivery':delivery}
    return render(request, 'edit_order.html', context)


def update_order(request, order_no, order_upd_no):
    order = Order.objects.all().filter(order_no=order_no)
    prod_name = request.POST['prod_name']
    prod1 = get_object_or_404(Product, prod_name=prod_name)
    stock = prod1.prod_stock
    earlier_quant = order[0].prod_quant
    new_quant = int(request.POST['quant'])
    result = stock - earlier_quant + new_quant
    prod1.prod_stock = result
    prod1.save()

    prod_quant = request.POST['quant']
    prod_rate = request.POST['rate']
    order = Order.objects.get(pk=order_upd_no)
    order.prod_quant = prod_quant
    order.prod_rate = prod_rate
    order.total = int(order.prod_quant) * int(order.prod_rate)
    order.save()

    order_supp_name = order.supp_name
    order_date = order.date
    order_total = order.total
    order_no = order.order_no

    context = {'order': order, 'order_supp_name': order_supp_name,
               'order_date': order_date, 'order_total': order_total, 'order_no': order_no
               }

    return HttpResponseRedirect(reverse('edit_order', args=[order_no]))


def save_order(request, order_no):
    return HttpResponseRedirect(reverse('order_list'))
