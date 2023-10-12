from phones.models import Phone
from django.http import HttpRequest
from django.shortcuts import render, redirect


def index(request):
    return redirect('catalog')


def show_catalog(request: HttpRequest):
    sort = request.GET.get('sort')
    match sort:
        case 'min_price' | 'max_price':
            sort_param = 'price'
            if sort == 'max_price':
                sort_param = '-' + sort_param
        case 'name':
            sort_param = sort
    if sort:
         phones = Phone.objects.all().order_by(sort_param)
    else:
        phones = Phone.objects.all()
    template = 'catalog.html'
    context = {
        'phones': phones,
        }
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.get(slug=slug)
    template = 'product.html'
    context = {
        'phone': phone,
        }
    return render(request, template, context)
