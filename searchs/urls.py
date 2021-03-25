from django.conf.urls import url

from .views import SearchView

app_name = "searchs"

urlpatterns = [
    url(r'^$', SearchView.as_view(), name='query'),
]
