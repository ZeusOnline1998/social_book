from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .managers import CustomUserManager
from django.template.defaultfilters import slugify
from django.urls import reverse
import magic
# Create your models here.

class CustomUser(AbstractUser):

    objects = CustomUserManager()

    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=True)
    address = models.CharField(max_length=255, null=True)
    birth_year = models.PositiveIntegerField(null=True)
    # age = models.PositiveIntegerField(null=True)

    # USERNAME_FIELD = 'email'

    @property
    def age(self):
        if self.birth_year:
            return datetime.today().year - self.birth_year
        else:
            return 'Not Specified'

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"username": self.username})

    @property
    def get_fullname(self):
        if not self.first_name:
            return 'Author Unspecified'
        return f'{self.first_name} {self.last_name}'

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.username)
    #     return super().save(*args, **kwargs)


class Book(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.PositiveIntegerField()
    published_date = models.PositiveIntegerField()
    visibility = models.BooleanField()
    file = models.FileField(default=None, upload_to='files/')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # slug = models.SlugField(null=False, unique=True)
    # file_type = models.CharField(default="pdf", max_length=50)

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.id})

