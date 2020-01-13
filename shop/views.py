from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Item, Order_Item, Address, Order
from .forms import ItemSearchForm

def homePage(request):
    if(request.user.is_authenticated):
        try:
            cartItems = Order_Item.objects.all().filter(User=request.user, Ordered=False)
            cartItemCount = len(cartItems)
        except Order_Item.DoesNotExist:
            cartItems = None
            cartItemCount = 0
    else:
        cartItemCount = 0
    return render(request, "main/home.html", {'cartItemsNum': cartItemCount})

def isValid(search):
    return search != '' and search is not None

def Items(request):
    #
    form = ItemSearchForm()

    #
    item_list = Item.objects.all().order_by('Price')
    search_name = request.GET.get('name')
    search_category = request.GET.get('category')
    search_min_price = request.GET.get('min_price')
    search_max_price = request.GET.get('max_price')
    search_min_discount = request.GET.get('min_discount')

    if search_name is None:
        search_name = ''
    if search_category is None:
        search_category = 18
    if search_min_price is None:
        search_min_price = ''
    if search_max_price is None:
        search_max_price = ''
    if search_min_discount is None:
        search_min_discount = ''

    if isValid(search_name):
        item_list = item_list.filter(Name__icontains=search_name)

    if isValid(search_category):
        if(search_category != 'None'):
            if int(search_category) >= 1 and int(search_category) <= 17:
                item_list = item_list.filter(Category=search_category)

    if isValid(search_min_price):
        if (search_min_price != 'None'):
            item_list = item_list.filter(Price__gte=search_min_price)

    if isValid(search_max_price):
        if (search_max_price != 'None'):
            item_list = item_list.filter(Price__lte=search_max_price)

    if isValid(search_min_discount):
        if (search_min_discount != 'None'):
            item_list = item_list.filter(Discount__gte=search_min_discount)

    #
    cartItem = request.POST.get("cart", "")
    if cartItem != '':
        itemForCart = Item.objects.get(pk=cartItem)
        try:
            p = Order_Item.objects.get(User=request.user, Item=itemForCart, Ordered=False)
            p.Quantity += 1
            p.save()
        except Order_Item.DoesNotExist:
            p = Order_Item(User=request.user, Item=itemForCart)
            p.save()

    #
    page = request.GET.get('page', 1)
    paginator = Paginator(item_list, 6)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'items': items,
        'search_name': search_name,
        'search_category': search_category,
        'min_discount': search_min_discount,
        'min_price': search_min_price,
        'max_price': search_max_price
    }

    #
    if(request.user.is_authenticated):
        cartItemRemove = request.POST.get("remove", "")
        print(cartItemRemove)
        if cartItemRemove != '':
            itemForCart = Item.objects.get(pk=cartItemRemove)
            print(itemForCart)
            try:
                p = Order_Item.objects.get(User=request.user, Item=itemForCart, Ordered=False)
                p.delete()
            except Order_Item.DoesNotExist:
                pass

        cartItemUpdateQ = request.POST.get("updateq", "")
        cartItemUpdateI = request.POST.get("updatei", "")
        if cartItemUpdateQ != '' and cartItemUpdateI != '':
            itemForCart = Item.objects.get(pk=cartItemUpdateI)
            try:
                p = Order_Item.objects.get(User=request.user, Item=itemForCart, Ordered=False)
                p.Quantity = int(cartItemUpdateQ)
                p.save()
            except Order_Item.DoesNotExist:
                pass

        #
        try:
            cartItems = Order_Item.objects.all().filter(User=request.user, Ordered=False)
            cartItemCount = len(cartItems)
        except Order_Item.DoesNotExist:
            cartItems = None
            cartItemCount = 0

        #
        context['cartItems'] = cartItems
        context['cartItemsNum'] = cartItemCount
    #
    return render(request, 'shop/items_view_filter.html', context)

global addressList

@login_required
def CartView(request):
    try:
        cartItems = Order_Item.objects.all().filter(User=request.user, Ordered=False)
    except Order_Item.DoesNotExist:
        cartItems = []

    orderState = 0

    cartItemUpdateQ = request.POST.get("updateq", "")
    cartItemUpdateI = request.POST.get("updatei", "")
    if cartItemUpdateQ != '' and cartItemUpdateI != '':
        itemForCart = Item.objects.get(pk=cartItemUpdateI)
        try:
            p = Order_Item.objects.get(User=request.user, Item=itemForCart, Ordered=False)
            p.Quantity = int(cartItemUpdateQ)
            p.save()
        except Order_Item.DoesNotExist:
            pass

    cartItemRemove = request.POST.get("remove", "")
    if cartItemRemove != '':
        itemForCart = Item.objects.get(pk=cartItemRemove)
        try:
            p = Order_Item.objects.get(User=request.user, Item=itemForCart, Ordered=False)
            p.delete()
        except Order_Item.DoesNotExist:
            pass

    cartItemsOrder = request.POST.get("order", "")
    if cartItemsOrder == request.user.username:
        orderState = 1

    UserAddresses = None
    try:
        UserAddresses = Address.objects.all().filter(User=request.user)
    except Address.DoesNotExist:
        pass


    orderAddId = request.POST.get("addId", "")

    if(orderAddId != ''):
        address = Address.objects.get(pk=orderAddId)
        orderState = 1
    else:
        address = None

    orderA = request.POST.get("apartment", "")
    orderS = request.POST.get("street", "")
    orderP = request.POST.get("pin", "")
    orderPay = request.POST.get("payment", "")

    if orderA != '' and orderS != '' and orderP != '' and orderPay != '':
        global addressList
        orderAddress = orderA
        orderStreet = orderS
        orderPin = orderP
        orderPayment = orderPay
        addressList = [orderAddress, orderStreet, orderPin, orderPayment]
        orderState = 2

    orderConfirm = request.POST.get("confirmorder", "")
    if orderConfirm != '':
        orderState = 3

    if orderState == 3:
        try:
            p = Address.objects.get(User=request.user, Apartment=addressList[0], Street=addressList[1], Zip=addressList[2])
        except Address.DoesNotExist:
            p = Address(User=request.user, Apartment=addressList[0], Street=addressList[1], Zip=addressList[2])
            p.save()

        o = Order(User=request.user, Address=p, Payment=int(addressList[3]))
        o.save()

        for item in cartItems:
            print(item)
            o.Items.add(item)
            o.save()
            item.Ordered = True
            item.save()
            itemS = Item.objects.get(pk=item.Item.pk)
            itemS.Stock -= item.Quantity
            itemS.save()

    try:
        cartItems = Order_Item.objects.all().filter(User=request.user, Ordered=False)
        cartItemsNum = len(cartItems)
    except Order_Item.DoesNotExist:
        cartItems = []
        cartItemsNum = 0

    price = 0
    for item in cartItems:
        price += item.get_total_item_price

    context = {
        'cartItems': cartItems,
        'orderState': orderState,
        'userAddresses': UserAddresses,
        'address': address,
        'price': price,
        'cartItemsNum': cartItemsNum
    }
    return render(request, 'shop/user_cart.html', context)

@login_required
def orders_view(request):
    try:
        orders = Order.objects.all().filter(User=request.user)
    except Order.DoesNotExist:
        orders = None

    try:
        cartItems = Order_Item.objects.all().filter(User=request.user, Ordered=False)
        cartItemsNum = len(cartItems)
    except Order_Item.DoesNotExist:
        cartItemsNum = 0

    context = {
        'orders': orders,
        'cartItemsNum': cartItemsNum
    }

    return render(request, 'shop/order_view.html', context)

@login_required
def order_view(request, pk):
    try:
        orders = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        orders = None

    try:
        cartItems = Order_Item.objects.all().filter(User=request.user, Ordered=False)
        cartItemsNum = len(cartItems)
    except Order_Item.DoesNotExist:
        cartItemsNum = 0

    context = {
        'order': orders,
        'cartItemsNum': cartItemsNum
    }

    return render(request, 'shop/order_detail.html', context)
