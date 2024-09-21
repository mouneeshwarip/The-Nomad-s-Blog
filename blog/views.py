from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Count
from .models import Post, Like, Share

# Create your views here.
class PostList(generic.ListView):
   # Annotate each post with the count of likes and shares
   queryset = Post.objects.all().annotate(
       like_count=Count('likes'),
       share_count=Count('shares')
   ).order_by('created_on') 
   template_name = "blog/index.html"   
   paginate_by = 6

def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    return render( request,"blog/post_detail.html",{"post": post})   



