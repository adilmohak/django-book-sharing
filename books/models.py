from django.db import models
from django.contrib.auth.views import get_user_model
from django.db.models.signals import pre_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.db.models import Q
# rating
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

# from django.core.validators import validate_slug

# from .utils import unique_slug_generator

User = get_user_model()

Art = "Art"
Biography = "Biography" 
Business = "Business" 
Children = "Children's" 
Christian = "Christian" 
Classics = "Classics" 
Comics = "Comics" 
Cookbooks = "Cookbooks" 
Ebooks = "Ebooks" 
Fantasy = "Fantasy" 
Fiction = "Fiction" 
Graphic_Novels = "Graphic Novels" 
Historical_Fiction = "Historical Fiction" 
History = "History" 
Horror = "Horror" 
Memoir = "Memoir" 
Music = "Music" 
Mystery = "Mystery" 
Nonfiction = "Nonfiction" 
Poetry = "Poetry" 
Psychology = "Psychology" 
Romance = "Romance" 
Science = "Science" 
Science_Fiction = "Science Fiction" 
Self_Help = "Self Help" 
Sports = "Sports" 
Thriller = "Thriller" 
Travel = "Travel" 
Young_Adult = "Young Adult"


class Genres(models.Model):
    genres = models.CharField(max_length=120)

    def __str__(self):
        return "{0}".format(self.genres)


class BookManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(summary__icontains=query)| 
                         Q(slug__icontains=query)| 
                         Q(author__icontains=query)|
                        #  Q(genres__icontains=query)|
                         Q(timestamp__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Book(models.Model):
    title = models.CharField(max_length=120)
    # slug = models.SlugField(blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=120, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    # genres = models.TextField(choices=GENRES, blank=True, null=True)
    genres = models.ManyToManyField(Genres, blank=True)
    cover_page = models.ImageField(upload_to='cover_pages/%Y/%m/%d', default='default_book_cover.png')
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating, related_query_name='books')

    # SLUG_REGEX = re.compile('^[-\w]+$')
    objects = BookManager()


    def __str__(self):
        return "{0}".format(self.title)

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'slug': self.slug})
    
    def is_owner(self, user):
        return self.user == user
    
    @property
    def avg_rating(self):
        avg = 0
        try:
            rating = Rating.objects.get(object_id=self.id)
            avg = rating.average
        except:
            pass
        return avg

    class Meta:
        ordering = ['-timestamp']

    # def save(self, *args, **kwargs):
    #     # value = str(self.title + self.id)
    #     # if self.slug == None:
    #     super().save(*args, **kwargs)
        
    #     value = "{obj_title}-{obj_id}".format(obj_title=self.title, obj_id=self.id)
    #     self.slug = slugify(value, allow_unicode=True)

# def pre_save_receiver(sender, instance, *args, **kwargs): 
#    if not instance.slug: 
#        instance.slug = unique_slug_generator(instance) 


# pre_save.connect(pre_save_receiver, sender = Book) 


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_review")
    review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'book']]


class BooklistManager(models.Manager):
    def new_or_get(self, request):
        # for key, value in self.request.session.items():
        #     print("\n", '{} => {}'.format(key, value), "\n")
        book_id = request.session.get("book_id", None)
        qs = self.get_queryset().filter(id=book_id)
        if qs.count() == 1:
            new_obj = False
            book_obj = qs.first()
            if request.user.is_authenticated and book_obj.user is None:
                book_obj.user = request.user
                book_obj.save()
        else:
            book_obj = Booklist.objects.new(user=request.user)
            new_obj = True
            # request.session['book_id'] = book_obj.id
        return book_obj, new_obj

    def new(self, user=None):
        # user_obj = None
        # if user is not None:
        if user.is_authenticated:
            user_obj = user
            if self.model.objects.filter(user=user_obj).count() > 0:
                return self.model.objects.get(user=user_obj)
            return self.model.objects.create(user=user_obj)
        return None


class Booklist(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True)

    objects = BooklistManager()

    def get_absolute_url(self):
        return reverse('books:user_booklist')
