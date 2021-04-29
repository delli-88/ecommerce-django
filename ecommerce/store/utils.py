import json
from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('cart:',cart)
    items = []
    order = {"get_cart_total":0,"get_cart_total_items":0, 'shipping':False}
    cartItems = order['get_cart_total_items']
    for i in cart:
        try:
            cartItems+=cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price*cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_total_items']+=cart[i]['quantity']
            item = {
                    'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                }
            items.append(item)
            if product.digital==False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems,'order':order,'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer,created = Customer.objects.get_or_create(user=request.user,name=request.user.username,email=request.user.email)
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_total_items
    else:
        cookieCartData = cookieCart(request)
        items = cookieCartData['items']
        order = cookieCartData['order']
        cartItems = cookieCartData['cartItems']
    return {'cartItems':cartItems,'order':order,'items':items}

def storeCategories(request):
    products = None
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.get_all_products_by_category_id(category_id)
    else:
        products = Product.get_all_products()
    return {'categories':categories, 'products':products}


def guestOrder(request, data):
    print("User is not logged in")

    print("COOKIES",request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer,created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer, completed = False)

    for item in items:
        product = Product.objects.get(id = item['product']['id'])
        orderItem = OrderItem.objects.create(product = product, order = order, quantity = item['quantity'])
    return customer,order
