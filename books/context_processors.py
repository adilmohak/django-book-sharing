from .models import *


def get_recommendation(request):
    books = Book.objects.filter(ratings__isnull=False).order_by('ratings__average')
    # booklist_obj = Booklist.objects.new_or_get(request)
    book_list_obj, new_obj = Booklist.objects.new_or_get(request)
    # context['user_booklist'] = book_list
    # print(book_list_obj.books.all())
    # books = Book.objects.all()
    # books = sorted(Book.objects.all(), key=lambda a: a.avg_rating, reverse=True)
    # print(books)
    recomended_books = set()

    if request.user.is_authenticated:
        # print("Authenticated user")
        booklist = None
        try:
            booklist = Booklist.objects.get(user=request.user)
            # bookLists = [book for book in booklist.books.all()]
        except:
            pass
        # ratings = Rating.objects.filter(object_id=request.user)
        # ratingBooks = [book.book for book in ratings]

        # if len(ratings) > 0:
        #     print("First check")
        #     for rating in ratings: 
        #         for book in books:
        #             book_obj = Book.objects.get(object_id=book.id)
        #             for genres in book_obj.genres.all():
        #                 if genres in book.genres.all():
        #                     if not(book in ratingBooks): 
        #                         recomended_books.add(book)
        if booklist is not None:
            # print("Second check")
            for book_obj in booklist.books.all():
                for book in books:
                    # if book.genres.all().count > 0:
                    for genres in book_obj.genres.all():
                        if genres in book.genres.all():
                            # if not(book in booklist.books.all()): 
                            recomended_books.add(book)
        if len(recomended_books) < 15:
            # print("Last check")
            # books = Book.objects.all()[:15]
            [recomended_books.add(book) for book in books]
    else:
        # print("Anonumes user")
        # books = Book.objects.all()[:15]
        [recomended_books.add(book) for book in books]
        
    sorted_recomended_books = sorted(recomended_books, key=lambda a: a.avg_rating, reverse=True)
    # print(recomended_books)

    return {'sorted_recomended_books': sorted_recomended_books, 'book_list_obj': book_list_obj}



# # class ContextRecomendBookList(generic.ListView):
# #     model = Book

# #     def get_queryset(self):
# #         # books = Book.objects.all()[:15]
# #         sorted_books = sorted(Book.objects.all(), key=lambda a: a.get_avg_rating, reverse=True)
# #         recomended_books = set()

# #         if self.request.user.is_authenticated:
# #             print("Authenticated user")
# #             booklist = None
# #             try:
# #                 booklist = BookList.objects.get(user=self.request.user)
# #                 bookLists = [book for book in booklist.books.all()]
# #             except:
# #                 pass
# #             ratings = Rating.objects.filter(user=self.request.user)
# #             ratingBooks = [book.book for book in ratings]

# #             if len(ratings) > 0:
# #                 print("First check")
# #                 for rating in ratings:
# #                     for book in sorted_books:
# #                         for genres in rating.book.genres.all():
# #                             if genres in book.genres.all():
# #                                 if not(book in ratingBooks): 
# #                                     recomended_books.add(book)
# #             elif booklist is not None:
# #                 print("Second check")
# #                 for book in booklist.books.all():
# #                     for book in sorted_books:
# #                         for genres in book.genres.all():
# #                             if genres in book.genres.all():
# #                                 if not(book in bookLists): 
# #                                     recomended_books.add(book)
# #             else:
# #                 print("Last check")
# #                 # books = Book.objects.all()[:15]
# #                 [recomended_books.add(book) for book in sorted_books]
# #         else:
# #             print("Anonumes user")
# #             # books = Book.objects.all()[:15]
# #             [recomended_books.add(book) for book in sorted_books]
        
# #         return recomended_books
