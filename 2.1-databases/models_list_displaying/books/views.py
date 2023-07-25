from django.shortcuts import render
from .models import Book
from datetime import datetime, timedelta
from django.core.paginator import Paginator
import json


def books_view(request):
    if not Book.objects.exists():
        Book.load_books_from_json()
    template = 'books/books_list.html'
    book = Book.objects.all()
    context = {'books': book}
    return render(request, template, context)

def books_sorted_date(request, date):
    try:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        books = []
        paginator = Paginator(books, 1)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        context = {
            'page': page,
            'requested_date': date,
            'prev_date': None,
            'next_date': None,
        }
        return render(request, 'books/books_by_date.html', context)

    next_date = parsed_date + timedelta(days=1)
    prev_date = parsed_date - timedelta(days=1)
    books = Book.objects.filter(pub_date__gte=parsed_date, pub_date__lt=next_date)

    file_path = "fixtures/books.json"
    with open(file_path, 'r', encoding='utf-8') as json_file:
        books_data = json.load(json_file)
    all_pub_dates = []
    for book_data in books_data:
        pub_date = datetime.strptime(book_data['fields']['pub_date'], '%Y-%m-%d').date()
        all_pub_dates.append(pub_date)
    all_pub_dates.sort()


    current_date_index = all_pub_dates.index(parsed_date.date())
    if current_date_index > 0:
        prev_date = all_pub_dates[current_date_index - 1]
    if current_date_index < len(all_pub_dates) - 1:
        next_date = all_pub_dates[current_date_index + 1]

    paginator = Paginator(books, 1)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'requested_date': date,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, 'books/books_by_date.html', context)