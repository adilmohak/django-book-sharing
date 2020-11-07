from django.conf.urls import url

from .views import BookRUDView, BookListView, UserBookList, RecomendBookList

app_name = 'api-books'

urlpatterns = [
    url(r'^$', BookListView.as_view(), name='books'),
    url(r'(?P<slug>[\w-]+)/detail/$', BookRUDView.as_view(), name='book-rud'),
    url(r'^user-book-list/$', UserBookList.as_view(), name='user-book-list'),
    url(r'^recommendation/$', RecomendBookList.as_view(), name='recommend'),
]




# from django.urls import path
# from rest_framework import routers
# from django.conf.urls import include

# router = routers.DefaultRouter()

# from .views import MovieViewSet, RatingViewSet, UserViewSet #8 15userviewset
# router.register('movies', MovieViewSet) #8
# router.register('ratings', RatingViewSet) #8
# router.register('users', UserViewSet) #15 for register and login

# app_name = 'api-books'

# urlpatterns = [
#     path('', include(router.urls)),
# ]
