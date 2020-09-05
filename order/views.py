from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from order.models import ShopCart, ShopCartForm
from product.models import Category, Product, Images, Comment



def index(request):
    return HttpResponse('Order Page')
@login_required(login_url='login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information

    checkproduct = ShopCart.objects.filter(product_id=id)  # Check product in shopcart
    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:  # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to ShopCart")
        return HttpResponseRedirect(url)
    else:  # if there is no post
        if control == 1:  # Update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  #
        else:  # Insert to shopcart
            data = ShopCart()  # model
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Product added to ShopCart")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty +=rs.quantity
        total += rs.product.price * rs.quantity
    #return HttpResponse(str(total))
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'total_qty': total_qty,

    }
    return render(request, 'shopcart.html', context)

@login_required(login_url='/login')#check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted from Shop Cart!")
    return HttpResponseRedirect("/shopcart")