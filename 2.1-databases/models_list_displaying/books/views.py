from datetime import date

from books.models import Book
from django.shortcuts import redirect, render


def index(request):
    return redirect('books')


def books_view(request):
    books = Book.objects.all().order_by('pub_date')
    template = 'books/books_list.html'
    context = {
        'books': books,
        }
    return render(request, template, context)


def books_pub_date_view(request, pub_date):
    books = Book.objects.filter(pub_date=pub_date)
    prev_books = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date')
    next_books = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date')
    prev_date, next_date = None, None
    if len(prev_books) > 0:
        prev_date = prev_books[0].pub_date
    if len(next_books) > 0:
        next_date = next_books[0].pub_date
    template = 'books/books_list.html'
    context = {
        'books': books,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, template, context)