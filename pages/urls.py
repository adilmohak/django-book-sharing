from django.conf.urls import url

from .views import ContactCreateView, NewsAndEventList
from django.views import generic

app_name = 'pages'

urlpatterns = [
    # url(r'^$', home_view, name='home'),
    url(r'^$', generic.TemplateView.as_view(template_name='pages/index.html'), name='home'),
    url(r'^about/$', generic.TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^contact/$', ContactCreateView.as_view(), name='contact'),
    url(r'^news-and-events/$', NewsAndEventList.as_view(), name='news_events'),
]
