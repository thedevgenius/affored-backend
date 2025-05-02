from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .utils import generate_random_color
# Create your models here.

class User(AbstractUser):
    username = None
    phone_regex = RegexValidator(regex=r'^\?1?\d{10,15}$', message="Phone number must be entered in the format: '9999999999'. Up to 15 digits allowed.")
    phone = models.CharField('Phone Number', max_length=17, unique=True, error_messages={'unique': "A user with that phone number already exists.",})

    profile_image = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    profile_color = models.CharField(max_length=7, default=generate_random_color(), blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

    def get_first_letter(self):
        return self.first_name[0].upper() if self.first_name else ''