from django.urls import path
from django.views import generic
from .views import (
    BookListView,
    BookDetailView,
    BookUpdateView,
    delete_book,
    user_booklist,
    user_booklist_update,
    BookCreateView,
    ReviewCreateView,
    review_update_view,
)

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="books"),
    path("create/", BookCreateView.as_view(), name="create"),
    path("review-create/", ReviewCreateView.as_view(), name="review_create"),
    path("<slug>/review-update/", review_update_view, name="review_update"),
    path(
        "recommendations/",
        generic.TemplateView.as_view(template_name="books/recommendation.html"),
        name="recommendation",
    ),
    path("<slug>/detail/", BookDetailView.as_view(), name="detail"),
    path("<slug>/update/", BookUpdateView.as_view(), name="update"),
    path("<slug>/delete/", delete_book, name="delete"),
    path("user-booklist/", user_booklist, name="user_booklist"),
    path("user/booklist/update/", user_booklist_update, name="user_booklist_update"),
]
