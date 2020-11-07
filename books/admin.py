from django.contrib import admin
from .models import Book, Genres


admin.site.register(Book)
admin.site.register(Genres)


# from django.contrib import admin
# from .models import Movie, Rating #6 make register

# admin.site.register(Movie) #6 new line
# admin.site.register(Rating) #6 new line
