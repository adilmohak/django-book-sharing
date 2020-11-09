from django.contrib import admin
from .models import Book, Genres, Review, Booklist


admin.site.register(Book)
admin.site.register(Booklist)
admin.site.register(Genres)
admin.site.register(Review)
