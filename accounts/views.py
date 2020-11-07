from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.views.generic import View, FormView

from django.http import JsonResponse
from django.core import serializers

from books.models import Book, Booklist
from .mixins import AjaxFormMixin
from .forms import UserUpdateForm, UserCreateForm
from .models import User


class CreateUserView(AjaxFormMixin, generic.FormView):
    # model = User
    # fields = ['email', 'password']
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = '/accounts/profile/'

    # def form_invalid(self, form):
    #     response = super(CreateUserView, self).form_invalid(form)
    #     if self.request.is_ajax():
    #         return JsonResponse(form.errors, status=400)
    #     else:
    #         return response

    # def form_valid(self, form):
    #     response = super(CreateUserView, self).form_invalid(form)
    #     print(form.cleaned_data)
    #     if self.request.is_ajax():
    #         print(form.cleaned_data)
    #         data = {
    #             'message': "Successfuly submitted form data."
    #         }
    #         return JsonResponse(data)
    #     else:
    #         return response

    # def get(self, *args, **kwargs):
    #     form = self.form_class()
    #     return render(self.request, self.template_name, 
    #         {"form": form})

    # def post(self, *args, **kwargs):
    #     print(self.request.is_ajax)
    #     if self.request.is_ajax and self.request.method == "POST":
    #         form = self.form_class(self.request.POST)
    #         if form.is_valid():
    #             instance = form.save()
    #             ser_instance = serializers.serialize('json', [ instance, ])
    #             # send to client side.
    #             return JsonResponse({"instance": ser_instance}, status=200)
    #         else:
    #             return JsonResponse({"error": form.errors}, status=400)

    #     return JsonResponse({"error": ""}, status=400)



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
    return render(request, 'accounts/user_profile.html', {'user_books': user_books, 'booklist_obj': booklist_obj})


@login_required
def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated!')
            return redirect('accounts:user_profile')
        else:
            messages.error(request, 'Please correct the error(s) below. ')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/user_setting.html', {
        'form': form,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed!')
            return redirect('accounts:user_profile')
        else:
            messages.error(request, 'Please correct the error(s) below. ')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {
        'form': form,
    })
