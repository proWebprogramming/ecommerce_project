from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

# Create your views here.
from home.models import Setting, ContactForm, ContactMessage
from product.models import Category, Product


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product_slider = Product.objects.all().order_by('id')[:4]
    product_latest = Product.objects.all().order_by('-id')[:8]
    product_picked = Product.objects.all().order_by('?')[:8]
    page = "home"
    context = {
        'setting': setting,
        'category': category,
        'product_slider': product_slider,
        'product_latest':product_latest,
        'product_picked': product_picked,
        'page': page,
    }
    return render(request,'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,}
    return render(request, 'about.html', context)


def contactus(request):
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Sizning xabaringiz yuborildi! Rahmat")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting,
               'form': form,}
    return render(request,'contact.html', context)


def category_product(request,id, slug):
    category = Category.objects.all()
    catdata = Category.objects.get(pk=1)
    products= Product.objects.filter(category_id=id)
    context = {
        'category': category,
        'catdata': catdata,
        'products': products,
    }
    return render(request, 'category_detail.html', context)
