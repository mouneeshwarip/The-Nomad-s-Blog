from django.contrib import admin
from .models import Post, Comment, Category, Like, Share
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Share)

