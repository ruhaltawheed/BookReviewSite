from django.contrib import admin
from .models import Book, Author, BookAuthor, Genre, BookGenre

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookAuthor)
admin.site.register(Genre)
admin.site.register(BookGenre)
