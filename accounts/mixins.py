from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login


class UserCreateAjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(UserCreateAjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(UserCreateAjaxFormMixin, self).form_valid(form)
        # user = form.save(commit=False)
        # password = form.cleaned_data['password']
        # print(password)
        # user.set_password(password)
        # user.save()

        # authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'],)
        # login(self.request, user)
        
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': "Successfully submitted form data."
            }
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            print(password)
            user.set_password(password)
            user.save()

            authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'],)
            login(self.request, user)
            ser_user = serializers.serialize('json', [ user, ])
            # send to client side.
            return JsonResponse({'user': ser_user}, status=200)
            # return JsonResponse(data)
        else:
            return response
