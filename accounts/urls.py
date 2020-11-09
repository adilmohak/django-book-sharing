from django.conf.urls import url
from django.urls import path, include
# from django.contrib.auth.views import (
#         LoginView, LogoutView, PasswordChangeView, PasswordResetView, 
#         PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, 
#     )

from django.contrib.auth import views as auth_view

from .views import CreateUserView, profile_page, user_update, change_password, UserDetailView # UserProfileView # CreateDoneView

app_name = "accounts"

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_account'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('update/', user_update, name='update_account'),
    # path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/', profile_page, name='user_profile'),
    path('change-password/', change_password, name='change_password'),

    # generic views
    # url(r'^', include('django.contrib.auth.urls')),

    url(r'^login/$', auth_view.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_view.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
]
