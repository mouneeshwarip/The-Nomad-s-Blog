from django.shortcuts import render
from django.views import generic
from django.db.models import Count
from .models import Post, Like, Share

# Create your views here.

class PostList(generic.ListView):
   queryset = Post.objects.all().annotate(
       like_count=Count('likes'),
       share_count=Count('shares')
   )
   template_name = "post_list.html"   



