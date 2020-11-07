from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from rest_framework import serializers
from django.contrib.auth.views import get_user_model

from star_ratings.models import Rating

from books.models import (Book, GENRES, BookList)
from accounts.serializers import UserSerializer

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
	# url = serializers.SerializerMethodField(read_only=True),
	url = serializers.HyperlinkedIdentityField(view_name='api-books:book-rud', lookup_field='slug')
	user = UserSerializer(read_only=True)
	# timestamp = serializers.DateField(default=timezone.now())
	owner = serializers.SerializerMethodField(read_only=True)
	# genres = serializers.MultipleChoiceField(choices=GENRES, label='Genres')
	class Meta:
		model = Book
		fields = [
			# 'url', # uniform resource indicator
			'id',
			'url',
			'slug',
			'user',
			'title',
			# 'content',
			'author', 
			'summary', 
			'genres', 
			'timestamp',
			'cover_page',
			# 'no_of_rate', 
			'avg_rating',
			'owner'
		]
		read_only_fields = ['id', 'user']
		ordering = ['-avg_rating']

	def save(self, *args, **kwargs):
		user = User.objects.first()
		book = super().save(user=user)
		return book

	def get_url(self, obj):
		request = self.context.get("request")
		return obj.get_api_url(request=request)

	def validate_title(self, value):
		qs = Book.objects.filter(title__iexact=value)
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("This title has already been used.")
		return value
	
	def get_owner(self, obj):
		request = self.context['request']
		if request.user.is_authenticated:
			if obj.user == request.user:
				return True
		return False


class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rating
		fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookList
		fields = '__all__'

















# from rest_framework import serializers
# from books.models import Movie, Rating
# from django.contrib.auth.models import User #14
# from rest_framework.authtoken.models import Token #17
# #14 for register and login
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password')
#         extra_kwargs = {'password': {'write_only': True, 'required': True}}
#         #16 validate data
#         def create(self, validated_data):
#             user = User.objects.create_user(**validated_data)
#             Token.objects.create(user=user)
#             return user
# class MovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = ('id', 'title', 'description', 'no_of_ratings', 'avg_rating')
# class RatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rating
#         fields = ('id', 'stars', 'user', 'movie')
