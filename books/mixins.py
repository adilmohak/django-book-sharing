from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages


class ReviewAjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(ReviewAjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(ReviewAjaxFormMixin, self).form_valid(form)

        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': "Successfully submitted form data."
            }
            review = form.save()
            ser_review = serializers.serialize('json', [ review, ])
            # send to client side.
            return JsonResponse({'review': ser_review}, status=200)
            # return JsonResponse(data)
        else:
            review = form.save()
            messages.success(self.request, 'Review submitted')
            next_ = self.request.POST.get('next')
            if next_:
                return redirect(next_)
            return response
