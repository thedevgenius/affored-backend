from django.db import models

from core.utils import generate_unique_slug
from .choices import STATE_CHOICES, COUNTRY_CHOICES
from django.core.exceptions import ValidationError
from django.contrib import messages
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.street_address    


