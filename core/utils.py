from django.utils.text import slugify
from django.db import models

def generate_unique_slug(instance, field_name):
    """
    Generate a unique slug for a given field in a Django model instance.
    
    Args:
        instance: The model instance for which to generate the slug.
        field_name: The name of the field to slugify.
        
    Returns:
        A unique slug string.
    """
    original_slug = slugify(getattr(instance, field_name))
    unique_slug = original_slug
    counter = 1

    while instance.__class__.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{original_slug}-{counter}"
        counter += 1

    return unique_slug