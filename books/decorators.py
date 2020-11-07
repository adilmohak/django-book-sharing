# from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.http import Http404
# from django.contrib.auth.decorators import user_passes_test
# from .models import Book


# def is_owner_required(slug, redirect_field_name=REDIRECT_FIELD_NAME, login_url=Http404):
#     """
#     Decorator for views that checks that the logged in user is a student,
#     redirects to the log-in page if necessary.
#     """
#     book = Book.objects.get(slug=slug)
#     if book.user == request.user:
#         actual_decorator = user_passes_test(
#             lambda u: u.is_active and u.is_student or u.is_superuser,
#             login_url=login_url,
#             redirect_field_name=redirect_field_name
#         )
#         if function:
#             return actual_decorator(function)
#     return actual_decorator

from django.contrib.auth.models import Permission


# class IsOwnerOrReadOnly(Permission.):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Instance must have an attribute named `owner`.
#         return obj.owner == request.user
