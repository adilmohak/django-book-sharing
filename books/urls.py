from django.urls import path
from django.conf.urls import url
from django.views import generic
from .views import BookListView, BookDetailView, book_update, delete_book, user_booklist, user_booklist_update, BookCreateView

app_name = 'books'

urlpatterns = [
    url(r'^$', BookListView.as_view(), name='books'),
    url(r'^create/$', BookCreateView.as_view(), name='create'),
    url(r'^recommendations/$', generic.TemplateView.as_view(template_name='books/recommendation.html'), name='recommendation'),
    url(r'^(?P<slug>[\w-]+)/detail/$', BookDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', book_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete_book, name='delete'),
    url(r'^user-booklist/$', user_booklist, name='user_booklist'),
    url(r'^user/booklist/update/$', user_booklist_update, name='user_booklist_update'),
]
