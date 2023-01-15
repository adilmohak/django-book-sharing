from django.urls import path

from .views import SearchView

app_name = "searchs"

urlpatterns = [
    path("", SearchView.as_view(), name="query"),
]
