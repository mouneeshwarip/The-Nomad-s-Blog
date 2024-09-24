from django.contrib import admin
from .models import About
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the About model. 

    - Uses Summernote for rich text editing of the 'content' field, 
      allowing the admin to create and edit HTML content with ease.
    """
    summernote_fields = ('content',)
