from django.db import models
from django.core.exceptions import ValidationError
import uuid

from core.utils import generate_unique_slug
from .choices import STATE_CHOICES, COUNTRY_CHOICES
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, editable=False, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        
        if self.parent and self.parent == self:
            raise ValidationError({'parent': "A category cannot be its own parent."})
    
    def save(self, *args, **kwargs):   
        if not self.slug:
            self.slug = generate_unique_slug(self, 'name')

        self.clean()
            
        super().save(*args, **kwargs)
    

class Address(models.Model):
    street_address = models.CharField(max_length=255, help_text="House No, Building, Street, Area")
    locality = models.CharField(max_length=100, help_text="Locality, Town, Village")
    city = models.CharField(max_length=100, help_text="City/District")
    state = models.CharField(max_length=100, choices=STATE_CHOICES)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default="IN")
    postal_code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.street_address


class Business(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, editable=False, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    address = models.OneToOneField('Address', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ManyToManyField('Category', blank=True)
    geohash = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)


    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = generate_unique_slug(self, 'name')
            if self.address and self.address.locality:
                locality = self.address.locality.lower()
                self.slug = f'{base_slug}-{locality}'
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}-{self.slug}'
    
