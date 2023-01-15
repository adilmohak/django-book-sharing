from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.views.generic import View, FormView

from django.http import JsonResponse
from django.core import serializers

from books.models import Book, Booklist

# from .mixins import UserCreateAjaxFormMixin
from .forms import UserUpdateForm, UserCreateForm
from .models import User


class CreateUserView(generic.FormView):
    # model = User
    # fields = ['email', 'password']
    form_class = UserCreateForm
    template_name = "accounts/user_form.html"
    success_url = "/accounts/profile/"

    def form_invalid(self, form):
        response = super(CreateUserView, self).form_invalid(form)
        return response

    def form_valid(self, form):
        response = super(CreateUserView, self).form_valid(form)

        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()

        authenticate(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        login(self.request, user)
        ser_user = serializers.serialize(
            "json",
            [
                user,
            ],
        )
        return response


# class CreateUserView(generic.CreateView):
#     model = User
#     fields = ['email', 'password']
#     success_url = '/accounts/profile/'

#     def form_valid(self, form):
#         super(CreateUserView, self).form_valid(form)
#         user = form.save()
#         authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'],)
#         login(self.request, user)
#         return redirect('accounts:user_profile')


@login_required
def profile_page(request):
    # user = request.user
    user_books = Book.objects.filter(user=request.user)
    booklist_obj = Booklist.objects.new_or_get(request)
    return render(
        request,
        "accounts/user_profile.html",
        {"user_books": user_books, "booklist_obj": booklist_obj},
    )


class UserDetailView(generic.DetailView):
    model = User
    template_name = "accounts/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        try:
            book_list_obj = Booklist.objects.get(user=self.get_object())
        except:
            book_list_obj = Booklist.objects.new(user=self.get_object())
        context["detail_user_booklist"] = book_list_obj
        context["detail_user_books"] = Book.objects.filter(user=self.get_object())
        return context


@login_required
def user_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated!")
            return redirect("accounts:user_profile")
        else:
            messages.error(request, "Please correct the error(s) below. ")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(
        request,
        "accounts/user_setting.html",
        {
            "form": form,
        },
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed!")
            return redirect("accounts:user_profile")
        else:
            messages.error(request, "Please correct the error(s) below. ")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "accounts/password_change.html",
        {
            "form": form,
        },
    )
