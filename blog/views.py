from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.views.generic import ListView
from django.http import HttpResponseRedirect
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

# Category list view
class CatListView(ListView):
    """
     Returns all published posts in :model:`blog.Category`
    and displays them on a page.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``category``
        Group of published posts in :model:`blog.Category`
    displayed on a page.
    """
    template_name = 'bewell_blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs[
                'category']).filter(status=1)
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='other')
    context = {
        "category_list": category_list,
    }
    return context