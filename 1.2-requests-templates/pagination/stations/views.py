import csv

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator


with open('data-398-2018-08-30.csv', 'r', encoding='utf-8') as file:
    content = csv.DictReader(file)
    PAGINATOR = Paginator([i for i in content], 20)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request: HttpRequest):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    context = {
         'bus_stations': PAGINATOR.get_page(page),
         'page': PAGINATOR.get_page(page),
    }
    return render(request, 'stations/index.html', context)
