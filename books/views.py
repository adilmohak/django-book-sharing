from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views import generic
from django.http import Http404
from django.contrib import messages
from django.utils.decorators import method_decorator
from star_ratings.models import Rating

# from .decorators import is_owner_required
from .models import Book, Booklist, Review
from .forms import BookForm, ReviewForm
from .mixins import ReviewAjaxFormMixin


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'

    def get_queryset(self):
        qs = sorted(Book.objects.all(), key=lambda a: a.avg_rating, reverse=True)
        # qs = Book.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        # book_list, new_obj = Booklist.objects.new_or_get(self.request)
        # context['user_booklist'] = book_list
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def get_object(self, queryset=None):
        obj = Book.objects.get(slug=self.kwargs['slug'])
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)
        # book_list, new_obj = Booklist.objects.new_or_get(self.request)
        # context['user_booklist'] = book_list
        context['is_owner'] = self.get_object().is_owner(self.request.user)
        context['reviews'] = Review.objects.filter(book=self.get_object())
        context['related_books'] = Book.objects.filter(user=self.get_object().user).order_by('-ratings')
        try:
            context['is_reviewed'] = Review.objects.get(user=self.request.user, book=self.get_object())
        except:
            context['is_reviewed'] = False
        return context


class BookCreateView(generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    
    def get_context_data(self, **kwargs):
        context = super(BookCreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form'] = BookForm(self.request.POST, initial={'user': self.request.user})
        else:
            context['form'] = BookForm(initial={'user': self.request.user})
        return context


# @login_required
# def book_create(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST, initial={'user': request.user})
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             messages.success(request, f'Book created successfuly.')
#             return redirect('books:detail', slug=obj.slug)
#         else:
#             print(form.errors)
#     else:
#         form = BookForm(initial={'user': request.user})
#     return render(request, 'books/book_form.html', {'form': form})


class BookUpdateView(generic.UpdateView):
    # lookup_field = 'slug'
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"


# @login_required
# def book_update(request, slug):
#     book = Book.objects.get(slug=slug)
#     if book.is_owner(request.user):
#         if request.method == 'POST':
#             form = BookForm(request.POST, request.FILES, instance=book)
#             if form.is_valid():
#                 obj = form.save(commit=False)
#                 obj.user = request.user
#                 obj.save()
#                 messages.success(request, f'Book updated.')
#                 return redirect('books:detail', slug=obj.slug)
#             else:
#                 print(form.errors)
#         else:
#             form = BookForm(instance=book)
#     else:
#         raise Http404
#     return render(request, 'books/book_form.html', {'form': form})


@login_required
def user_booklist(request):
    booklist_obj = Booklist.objects.get(user=request.user)
    return render(request, "books/user_booklist.html", {'booklist': booklist_obj})


@login_required
def user_booklist_update(request):
    print("ajax", request.is_ajax())
    book_id = request.POST.get('book_id')

    # if book_id is not None:
    try:
        book_obj = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        print("Show message to user, book is gone?")
        return redirect("books:user_booklist")
    booklist_obj, new_obj = Booklist.objects.new_or_get(request)
    if book_obj in booklist_obj.books.all():
        booklist_obj.books.remove(book_obj)
        added = False
    else:
        booklist_obj.books.add(book_obj) # booklist_obj.books.add(booklist_id)
        added = True
    request.session['booklist_items'] = booklist_obj.books.count()
    # return redirect(booklist_obj.get_absolute_url())
    next_ = request.POST.get('next')
    if next_ is not None: 
        return redirect(next_)
    return redirect("books:user_booklist")


# @method_decorator([login_required], name='dispatch')
# class BookUpdateView(generic.UpdateView):
#     model = Book
#     form_class = BookForm
#     book = Book.objects.get(slug=self.kwargs['slug'])

#     def get_context_data(self, **kwargs):
#         context = super(BookUpdateView, self).get_context_data(**kwargs)
#         return context['form'] = BookForm(initial=book)

#     def get_object(self):
#         print(book.is_owner(self.request.user))
#         if book.is_owner(self.request.user):
#             book = Book.objects.get(slug=self.kwargs['slug'])
#         else:
#             raise Http404


@login_required
def delete_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if (book.user == request.user):
        book.delete()
        messages.success(request, 'Book deleted.')
        return redirect('accounts:user_profile')
    else:
        raise Http404


# @method_decorator[@login_required]
class ReviewCreateView(ReviewAjaxFormMixin, generic.CreateView):
    model = Review
    # fields = '__all__'
    form_class = ReviewForm
    success_url = '/books/'


@login_required
def review_update_view(request, slug):
    book = get_object_or_404(Book, slug=slug)
    review = get_object_or_404(Review, book=book.id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated')
            return redirect('books:detail', slug=book.slug)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'books/review_form.html', {'form': form})
