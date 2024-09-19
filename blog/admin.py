from django.contrib import admin
from .models import Post, Comment, Category, Like, Share
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

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

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Share)

