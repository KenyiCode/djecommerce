from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        "products": products,
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {
        "items": items,
        "order": order,
        'cartItems': cartItems,
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {
        "order": order,
        "items": items,
        "cartItems": cartItems,
    }
    return render(request, 'store/checkout.html', context)

def viewItem(request, product_id):
    data = cartData(request)
    product = Product.objects.get(id=product_id)
    print(product)

    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {
        "product": product,
        "order": order,
        "items": items,
        "cartItems": cartItems,
    }
    return render(request, 'store/view.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action: ', action)
    print("Product ID: ", productID)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if (orderItem.quantity <= 0):
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

    else:
        customer, order = guestOrder(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)