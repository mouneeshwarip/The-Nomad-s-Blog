from django.contrib import admin
from .models import Post, Comment, Category, Like, TravelStory
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the Post model, allowing customization of
    the admin interface. 

    - Displays the title, slug, status, and timestamps in the list view.
    - Enables search functionality based on the post title.
    - Filters posts by status.
    - Automatically generates the slug based on the title.
    - Uses Summernote for rich text editing of the content field.
    - Displays a thumbnail of the featured image in the admin interface.
    """
    list_display = ('title', 'slug', 'status', 'created_on', 'updated_on')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    def featured_image_display(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.featured_image.url)
        return 'No Image'

    featured_image_display.short_description = 'Featured Image'

@admin.register(TravelStory)
class TravelStoryAdmin(SummernoteModelAdmin):
    '''
    Register the TravelStory model.
    Customize Admin Interface.
    '''
    list_display = ('title', 'author', 'status', 'created_on', 'updated_on')
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)} 
    summernote_fields = ('content',)  

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Like)

