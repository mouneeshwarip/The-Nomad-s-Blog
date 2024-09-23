from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.db.models import Count
from .models import Post, Like, Share, Category

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
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    return render(request,"blog/post_detail.html",
      {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
      },
    )
class CatListView(ListView):
    """
    Displays all published posts within a specific category.
    """
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'  # This will be the variable used in the template

    def get_queryset(self):
        # Filter posts based on the category name passed in the URL
        category = self.kwargs['category']
        return Post.objects.filter(category__name=category,status=1).annotate(
            like_count=Count('likes'),
            share_count=Count('shares')
        )


    def get_context_data(self, **kwargs):
        # Add the category name to the context for display
        context = super().get_context_data(**kwargs)
        context['cat'] = self.kwargs.get('category')
       
        return context
  

   