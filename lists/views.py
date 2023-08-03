from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import *
from datetime import date, timedelta

# Create your views here.

#########
#  Lists

@login_required
def lists(request):
    
    #show 5 lists on every view
    lists = List.objects.filter(user=request.user).order_by('-id')
    products_w_price = ProductWPrice.objects.filter(user=request.user)
        
    list_form = ListForm()
    store_form = StoreForm()

    paginator = Paginator(lists, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_stores = Store.objects.filter(user = request.user)

    # Que el select field solo muestre los productos del usuario
    list_form.fields['store'].queryset = user_stores

    if request.method == 'POST':
        if "create_store_btn" in request.POST:
            form = StoreForm(request.POST, request.FILES)

        else:
            form = ListForm(request.POST, request.FILES)


        if form.is_valid:
            auth = form.save(commit=False)
            auth.user = request.user
            auth.save()

    
            

    context = {
        'lists' : lists,
        'list_form' : list_form,
        'store_form' : store_form,
        'products_w_price' : products_w_price,
        'page_obj' : page_obj,

    }

    return render(request, 'lists/lists.html', context)


@login_required
def list_info(request, primary_key_list):
    products_w_price = ProductWPrice.objects.filter(list = primary_key_list)
    actual_list = List.objects.get(id = primary_key_list)
    user_products = Product.objects.filter(user=request.user)


    if(actual_list.user != request.user):
        return redirect('lists')

    product_w_price_form = ProductWPriceForm()
    unit_form = UnitForm()
    summed_total = 0

    # Que el select field solo muestre los productos del usuario
    product_w_price_form.fields['product'].queryset = user_products

    for i in products_w_price:
        summed_total += i.price

    summed_total = round(summed_total, 2)

    #preview mechanics
    if(products_w_price):
        preview_products_w_price = products_w_price.filter(is_preview=True)
        last_product_w_price = products_w_price[len(products_w_price) -1]
        if(len(preview_products_w_price) > 2):
            update = False
            remove_product = last_product_w_price
            for preview_product in preview_products_w_price:
                if(last_product_w_price.price > preview_product.price):
                    if(update == False):
                        update = True
                        remove_product = preview_product
                    elif(update == True and remove_product.price > preview_product.price):
                        remove_product = preview_product

            if(update == True):
                remove_product.is_preview = False
                remove_product.save()
            else:
                last_product_w_price.is_preview = False
                last_product_w_price.save()

    if request.method == 'POST':

        if 'product_w_price_form' in request.POST:
            product_w_price_form = ProductWPriceForm(request.POST, request.FILES)
            if product_w_price_form.is_valid:
                product = product_w_price_form.save(commit=False)
                product.list = actual_list
                product.unit_price = round(float(product.price)/float(product.amount), 2)
                product.user = request.user
                product.save()

        return redirect('list_info', primary_key_list)

    context = {
        'products_w_price' : products_w_price,
        'product_w_price_form' : product_w_price_form,
        'actual_list' : actual_list,
        'summed_total' : summed_total,
        
    }

    return render(request, 'lists/list_info.html', context)


@login_required
def delete_list(request, primary_key_list):
    list = List.objects.get(id=primary_key_list)

    if(list.user != request.user):
        return redirect('lists')

    products_w_price = ProductWPrice.objects.filter(list=list)
    products_w_price.delete()
    list.delete()
    return redirect('lists')



###########
#  Poducts

@login_required
def products(request):
    products = Product.objects.filter(user=request.user).order_by('-id')
    product_form = ProductForm()
    unit_form = UnitForm()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':

        if 'product_form' in request.POST:
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid:
                product = product_form.save(commit=False)
                product.product_name_w_brand = product.product_name + " - " + product.brand
                product.user = request.user
                product.save()

        elif 'unit_form' in request.POST:
            unit_form = UnitForm(request.POST)
            if unit_form.is_valid:
                unit = unit_form.save(commit=False)
                unit.user = request.user
                unit.save()

        return redirect('products')

    context = {
        'products' : products,
        'product_form' : product_form,
        'unit_form' : unit_form,
        'page_obj' : page_obj,
    }

    return render(request, 'lists/products.html', context)


@login_required
def product_data(request, primary_key_product):
    product = Product.objects.get(id=primary_key_product)

    if(product.user != request.user):
        return redirect('products')

    products_same_name = Product.objects.filter(user=request.user, product_name=product.product_name)
    product_instances = ProductWPrice.objects.filter(user=request.user, product__in=products_same_name)
    products_same_brand = Product.objects.filter(user=request.user, brand = product.brand)
    product_instances_same_brand = ProductWPrice.objects.filter(user=request.user, product__in=products_same_brand)
    filter_product_data_form = FilterProductDataForm()
    amount_bought = len(product_instances_same_brand)

    if product_instances_same_brand:
        end_date = product_instances_same_brand[len(product_instances_same_brand) - 1].list.date + timedelta(days = 1)
        # end_date = date.today()
        start_date = end_date - timedelta(days = 30)
        end_date = end_date.strftime('%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
    else:
        end_date = date.today()
        start_date = date.today()

    total_spendings = 0
    unit_price_average = 0
    unit_price_change = 0


    for i in product_instances_same_brand:
        total_spendings += i.price
        unit_price_average += i.unit_price
        
    
    if amount_bought > 0:
        unit_price_average = round(unit_price_average/amount_bought, 2)
        first_price = product_instances_same_brand[0].unit_price
        last_price = product_instances_same_brand[len(product_instances_same_brand) - 1].unit_price
        unit_price_change = round((last_price/first_price) - 1.0, 2)

    context = {
        'product' : product,
        'product_instances' : product_instances,
        'filter_product_data_form' : filter_product_data_form,
        'product_instances_same_brand' : product_instances_same_brand,
        'total_spendings' : total_spendings,
        'amount_bought' : amount_bought,
        'unit_price_average' : unit_price_average,
        'unit_price_change' : unit_price_change,
        'end_date' : end_date,
        'start_date' : start_date,

    }

    return render(request, 'lists/product_data.html', context)


@login_required
def edit_products(request):
    products = Product.objects.filter(user = request.user).order_by('-id')
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {
        'products' : products,
        'page_obj' : page_obj,

    }
    return render(request, 'lists/edit_products.html', context)


@login_required
def edit_product(request, primary_key_product):
    product = Product.objects.get(id=primary_key_product)

    if(product.user != request.user):
        return redirect('products')

    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid:
            form.save()
            return redirect('edit_products')
    
    context = {
        'product' : product,
        'product_form' : form,
    }

    return render(request, 'lists/edit_product.html', context)


@login_required
def delete_product_w_price(request, primary_key_product_w_price, primary_key_list):
    product_w_price = ProductWPrice.objects.get(id=primary_key_product_w_price)

    if(product_w_price.user != request.user):
        return redirect('lists')

    product_w_price.delete()
    return redirect('list_info', primary_key_list)


@login_required
def delete_product(request, primary_key_product):
    product = Product.objects.get(id=primary_key_product)

    if(product.user != request.user):
        return redirect('products')

    product.delete()
    return redirect('products')


#######
#  Stores

@login_required
def edit_stores(request):
    stores = Store.objects.filter(user=request.user).order_by('-id')

    paginator = Paginator(stores, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'stores' : stores,
        'page_obj' : page_obj,
    }

    return render(request, 'lists/edit_stores.html', context)


@login_required
def edit_store(request, primary_key_store):
    store = Store.objects.get(id = primary_key_store)

    if(store.user != request.user):
        return redirect('products')

    store_form = StoreForm(instance=store)

    if request.method == 'POST':
        store_form = StoreForm(request.POST, request.FILES, instance=store)
        if store_form.is_valid:
            store_form.save()
            return redirect('edit_stores')
    
    context = {
        'store' : store,
        'store_form' : store_form,
    }

    return render(request, "lists/edit_store.html", context)


@login_required
def delete_store(request, primary_key_store):
    store = Store.objects.get(id=primary_key_store)

    if(store.user != request.user):
        return redirect('lists')

    store.delete()
    return redirect('edit_stores')



######
#  Units

@login_required
def edit_units(request):
    units = Unit.objects.filter(user = request.user).order_by('-id')

    paginator = Paginator(units, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'units' : units,
        'page_obj' : page_obj,
    }

    return render(request, 'lists/edit_units.html', context)


@login_required
def edit_unit(request, primary_key_unit):
    unit = Unit.objects.get(id = primary_key_unit)

    if(unit.user != request.user):
        return redirect('products')

    unit_form = UnitForm(instance=unit)

    if request.method == 'POST':
        unit_form = UnitForm(request.POST, instance=unit)
        if unit_form.is_valid:
            unit_form.save()
            return redirect('edit_units')
    
    context = {
        'unit' : unit,
        'unit_form' : unit_form,
    }

    return render(request, "lists/edit_unit.html", context)



@login_required
def delete_unit(request, primary_key_unit):
    unit = Unit.objects.get(id=primary_key_unit)

    if(unit.user != request.user):
        return redirect('lists')

    unit.delete()
    return redirect('edit_units')


#######
#  Test

def create_test(request):
    Store(1, 'H-E-B (Chipinque)', 'Chipinque', 'images/H-E-B_Logo.png').save()
    Store(2, 'Soriana (San Pedro)', 'San Pedro', 'images/Soriana_Logo.png').save()

    List(1, '2023-01-10', '19:00:34.9', r"images\recibo_heb.jpg", 1, 940).save()
    List(2, '2023-01-10', '19:00:34.9', r'images\recibo_heb.jpg', 2, 780).save()

    
    Product(1, 'Huevos', 'images\docena_huevos.jpeg', 'Bachoco', 'Huevos - Bachoco').save()
    Product(2, 'Manzanas', 'images\manzanas.jpeg', 'Varela', 'Manzanas - Varela').save()

    Unit(1, 'Piece', 1).save()
    Unit(2, 'g', 100).save()

    ProductWPrice(1, 1, 100, 1, True, 12, 1, 10).save()
    ProductWPrice(2, 1, 110, 1, True, 12, 1, 11).save()

    for i in range(3, 15):
        ProductWPrice(i, 1, i+100, 1, False, 12, 1, 11).save()

    return redirect('lists')




