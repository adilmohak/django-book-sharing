from django.urls import path

from .views import ContactCreateView, NewsAndEventList
from django.views import generic

app_name = 'pages'

urlpatterns = [
    # path('', home_view, name='home'),
    path('', generic.TemplateView.as_view(template_name='pages/index.html'), name='home'),
    path('about/', generic.TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('news-and-events/', NewsAndEventList.as_view(), name='news_events'),
]
