from django.shortcuts import render, redirect
from django.urls import reverse
from pagination.settings import BUS_STATION_CSV
from django.core.paginator import Paginator
import csv

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(BUS_STATION_CSV, 1)
    page = paginator.get_page(page_number)
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    with open(BUS_STATION_CSV, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        stations_list = list(reader)

    context = {
        'bus_stations': stations_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
