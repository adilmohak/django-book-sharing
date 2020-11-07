from django.conf.urls import url
from django.urls import path, include
# from django.contrib.auth.views import (
#         LoginView, LogoutView, PasswordChangeView, PasswordResetView, 
#         PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, 
#     )

from django.contrib.auth import views as auth_view

from .views import CreateUserView, profile_page, user_update, change_password # UserProfileView # CreateDoneView
from .forms import EmailValidationOnForgotPassword

app_name = "accounts"

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_account'),
    path('update/', user_update, name='update_account'),
    # path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/', profile_page, name='user_profile'),
    path('change-password/', change_password, name='change_password'),

    # path('create-done', CreateDoneView.as_view(), name='create-done')

    # generic views
    # url(r'^', include('django.contrib.auth.urls')),

    url(r'^login/$', auth_view.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_view.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),

    url(r'^password-reset/$', auth_view.PasswordResetView.as_view(
        form_class=EmailValidationOnForgotPassword,
        template_name='registration/password_reset.html'
    ), name='password_reset'),

    url(r'^password-reset/done/$', auth_view.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    url(r'^password-reset-confirm/<uidb64>/<token>/$', auth_view.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    url(r'^password-reset-complete/$', auth_view.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete')
]
