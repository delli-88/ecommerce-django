from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from .models import *
from .forms import *
from .utils import cookieCart,cartData,storeCategories,guestOrder
import json
import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def store(request):
    storeCategoriesData = storeCategories(request)
    categories = storeCategoriesData['categories']
    products = storeCategoriesData['products']

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    product_dict = {"products":products,"categories":categories,"cartItems":cartItems,'order':order,'items':items}
    return render(request,"store/store.html",product_dict)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    itemsDict = {"items":items,"order":order,"cartItems":cartItems}
    if cartItems>0:
        return render(request,"store/cart.html",itemsDict)
    else:
        return render(request,"store/emptycart.html",itemsDict)


def emptycart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    itemsDict = {"items":items,"order":order,"cartItems":cartItems}
    return render(request,"store/emptycart.html",itemsDict)

def checkOut(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    itemsDict = {"items":items,"order":order,"cartItems":cartItems}
    return render(request,"store/checkOut.html",itemsDict)

def main(request):
    return render(request,"store/main.htlm",{})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId',productId)
    print('action',action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer = customer,completed = False)
    orderItem,created = OrderItem.objects.get_or_create(product = product,order = order)

    if action=='add':
        orderItem.quantity+=1
    elif action=='remove':
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,completed = False)
    else:
        customer,order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.completed = True
    order.save()

    if order.shipping==True:
        ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],)

    return JsonResponse('Payment Complete', safe=False)


def user_register(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    registered = False
    if request.method=="POST":
        user_form = UserForm(data = request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            customer,created = Customer.objects.get_or_create(user=user,name=user.username,email=user.email)
            customer.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,"store/user_register.html",
    {"user_form":user_form,"registered":registered,"items":items,"order":order,"cartItems":cartItems})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('store'))


def user_login(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('store'))
            else:
                return HttpResponse("Not active")
        else:
            return HttpResponseRedirect(reverse('store:invalid_login'))
    else:
        return render(request,"store/user_login.html",{"items":items,"order":order,"cartItems":cartItems})

def invalid_login(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    return render(request,"store/invalid_login.html",{"items":items,"order":order,"cartItems":cartItems})
