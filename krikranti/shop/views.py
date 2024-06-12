from django.contrib import messages
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product, order, OrderUpdate, Category, Sub_category
from users.models import Contact
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def index(request):
    categories = Category.objects.all()
    subcategories = Sub_category.objects.all()

    selected_category_id = request.GET.get('category_id')
    selected_subcategory_id = request.GET.get('subcategory_id')

    # Filter products based on selected category and subcategory
    product_objects = Product.objects.all()

    if selected_category_id:
        product_objects = product_objects.filter(category_id=selected_category_id)

    if selected_subcategory_id:
        product_objects = product_objects.filter(sub_category_id=selected_subcategory_id)

    # Search code
    item_name = request.GET.get('item_name')
    if item_name:
        product_objects = product_objects.filter(name__icontains=item_name)

    # If no category or subcategory is selected, select a random subset of products
    if not selected_category_id and not selected_subcategory_id:
        random_products = random.sample(list(product_objects), min(5, len(product_objects)))
    else:
        random_products = []

    return render(request, 'shop/index.html', {
        'product_objects': product_objects,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category_id': int(selected_category_id) if selected_category_id else None,
        'selected_subcategory_id': int(selected_subcategory_id) if selected_subcategory_id else None,
        'random_products': random_products,
    })


def detail(request, id):
    products_object = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': products_object})


def about(request):
    product_objects = Product.objects.all()
    return render(request, 'shop/about.html', {'product_objects': product_objects})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        desc = request.POST.get('desc', '')
        contacts = Contact(name=name, email=email, phone_number=phone_number, desc=desc)
        contacts.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            orders = order.objects.filter(order_id=orderId, email=email)
            if len(orders) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": orders[0].item_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"no item"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracking.html')


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        item_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        province = request.POST.get('province', '')
        district = request.POST.get('district', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip', '')
        # Create and save the Order object within the POST block
        orders = order(item_json=item_json, name=name, email=email, phone=phone, province=province, district=district,
                       city=city, zip_code=zip_code, amount=amount)
        orders.save()
        update = OrderUpdate(order_id=orders.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = orders.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    # ---- transfer amount to paytm
    return render(request, 'shop/checkout.html')


