"""djBooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

# from django.conf.urls import include # 2 new line
from rest_framework.authtoken.views import obtain_auth_token #11

urlpatterns = [
    path('', include('pages.urls', namespace="pages")),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    # path('api/books/', include('books.api.urls', namespace="api-books")),
    # path('admin/', admin.site.urls),

    # path('api/', include('books.api.urls')), # 3 new line
    path('auth/', obtain_auth_token), # 11
    
    # path('', TemplateView.as_view(template_name='react.html')),
    # path('walking', TemplateView.as_view(template_name='walking.html')),
    # re_path(r'^books/', TemplateView.as_view(template_name='react.html')),

    # path('api/books/', include('books.api.urls', namespace='api-books')),
    path('books/', include('books.urls', namespace='books')),
    
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
