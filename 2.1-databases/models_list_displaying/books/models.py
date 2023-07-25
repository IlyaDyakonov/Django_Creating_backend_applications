from django.db import models
import json
from datetime import datetime


class Book(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    author = models.CharField(max_length=64, verbose_name='Автор')
    pub_date = models.DateField(verbose_name='Дата публикации')

    def __str__(self):
        return self.name + " " + self.author

    @staticmethod
    def load_books_from_json():
        file_path = "fixtures/books.json"
        with open(file_path, 'r', encoding='utf-8') as json_file:
            books_data = json.load(json_file)

        for book_data in books_data:
            name = book_data['fields']['name']
            author = book_data['fields']['author']
            pub_date = datetime.strptime(book_data['fields']['pub_date'], '%Y-%m-%d').date()

            Book.objects.create(name=name, author=author, pub_date=pub_date)
