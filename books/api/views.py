from django.shortcuts import render
from django.http import JsonResponse

from django.db.models import Q
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from books.models import Book, Rating, BookList
from .serializers import BookSerializer, RatingSerializer, BookListSerializer
from .permissions import IsOwnerOrReadOnly
from accounts.models import User


class BookListView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'slug'
    serializer_class = BookSerializer
    permission_class = [IsOwnerOrReadOnly]
    # queryset = Book.objects.all()

    def get_queryset(self):
        queryset = Book.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            queryset = queryset.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def put(self):
        return self.update(request, *args, **kwargs)
    def patch(self):
        return self.update(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class BookRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserBookList(generics.ListAPIView):
    serializer_class = BookListSerializer

    def get_queryset(self):
        queryset = BookList.objects.filter(user=self.request.user)
        return queryset


class RecomendBookList(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        books = Book.objects.all()[:15]
        recomended_books = set()

        if self.request.user.is_authenticated:
            print("Authenticated user")
            booklist = None
            try:
                booklist = BookList.objects.get(user=self.request.user)
                bookLists = [book for book in booklist.book.all()]
            except:
                pass
            ratings = Rating.objects.filter(user=self.request.user).order_by('-stars')
            ratingBooks = [book.book for book in ratings]

            if len(ratings) > 0:
                print("First check")
                for rating in ratings:
                    for book in books:
                        for genres in rating.book.genres.all():
                            if genres in book.genres.all():
                                if not(book in ratingBooks): 
                                    recomended_books.add(book)

            elif booklist is not None:
                print("Second check")
                for book in booklist.book.all():
                    for book in books:
                        for genres in book.genres.all():
                            if genres in book.genres.all():
                                if not(book in bookLists): 
                                    recomended_books.add(book)
            
            else:
                print("Last check")
                books = Book.objects.all()[:15]
                [recomended_books.add(book) for book in books]
        else:
            print("Anonumes user")
            books = Book.objects.all()[:15]
            [recomended_books.add(book) for book in books]
        
        return recomended_books


# def book_recomendations_view(request):
    
#     booklist = BookList.objects.get(user=request.user)
#     books = Book.objects.all()

#     # book_recomend = []
#     # index = 0
#     recomended_books = [{"title": book.title} for book in books if book in booklist.book.all()]
#     # for book in books:
#     #     if book in booklist.book.all():
#     #         book_recomend.insert(index, book)
#     #         index += 1

#     # print(book_recomend)
#     # recomended_books = [{'title': x.title} for x in book_recomend]
#     print(recomended_books)

#     return JsonResponse(recomended_books, safe=False)
















# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny, )
# # Create your views here. 7
# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     authentication_classes = (TokenAuthentication, ) #12
#     permission_classes = (IsAuthenticated, ) #19
#     #8
#     @action(detail=True, methods=['POST'])
#     def rate_movie(self, request, pk=None):
#         if 'stars' in request.data:
#             movie = Movie.objects.get(id=pk)
#             stars = request.data['stars']
#             user = request.user #12
#             try:
#                 rating = Rating.objects.get(user=user.id,
# movie=movie.id)
#                 rating.stars = stars
#                 rating.save()
#                 serializer = RatingSerializer(rating, many=False)
#                 response = {'message': 'rating updated', 'result': serializer.data}
#                 return Response(response, status=status.HTTP_200_OK)
#             except:
#                 rating = Rating.objects.create(user=user, movie=movie, stars=stars)
#                 serializer = RatingSerializer(rating, many=False)
#                 response = {'message': 'rating created', 'result': serializer.data}
#                 return Response(response, status=status.HTTP_200_OK)
#         else:
#             response = {'message': 'you need to provide stars'}
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)
# class RatingViewSet(viewsets.ModelViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     authentication_classes = (TokenAuthentication, ) #12
#     permission_classes = (IsAuthenticated, ) #19
#     #20
#     def update(self, request, *args, **kwargs):
#         response = {'message': 'you cant update rating like that'}
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)
#     def create(self, request, *args, **kwargs):
#         response = {'message': 'you cant create rating like that'}
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)
