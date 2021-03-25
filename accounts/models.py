from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, AbstractUser)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email,password=password,**extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(email__icontains=query) | 
                         Q(name__icontains=query)| 
                         Q(location__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    name = models.CharField(max_length=100, blank=True, null=True)
    # last_name = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_profile_pic/%Y/%m/%d', default='default_profile_pic.png')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        full_name = self.email
        if self.name:
            full_name = self.name
        return full_name

    @property
    def get_absolute_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.id})
    
    # @property
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    # @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
