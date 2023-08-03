from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .managers import CustomUserManager
# Create your models here.
class CustomUser(AbstractUser):

    objects = CustomUserManager()

    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=True)
    address = models.CharField(max_length=255, null=True)
    birth_year = models.PositiveIntegerField(null=True)
    age = models.PositiveIntegerField(null=True)

    # USERNAME_FIELD = 'email'

    # @property
    # def age(self):
    #     if self.birth_year:
    #         self.age = datetime.today().year - self.birth_year
    #     else:
    #         self.age = 0

    def save(self, *args, **kwargs):
        self.age = datetime.today().year - self.birth_year
        return super().save(*args, **kwargs)
