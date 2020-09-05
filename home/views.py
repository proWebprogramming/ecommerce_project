import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage
from product.models import Category, Product, Images, Comment


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
    setting = Setting.objects.all()
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
    setting = Setting.objects.all()
    form = ContactForm
    context = {'setting': setting,
               'form': form,}
    return render(request,'contact.html', context)


def category_product(request,id, slug):
    category = Category.objects.all()
    catdata = Category.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)
    context = {
        'category': category,
        'catdata': catdata,
        'products': products,
    }
    return render(request, 'category_detail.html', context)

def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {
        'category': category,
        'product': product,
        'images': images,
        'comments': comments,
    }
    return render(request, 'product_detail.html', context)


def search(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {
                'products': products,
                'query': query,
                'category': category,
            }
            return render(request, 'search.html', context)
    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            products_json = {}
            products_json = rs.title
            results.append(products_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
