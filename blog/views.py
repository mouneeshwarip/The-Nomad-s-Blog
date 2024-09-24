from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.db.models import Count
from .models import Post, Like, Category, Comment
from .forms import CommentForm

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
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
    like_count = post.likes.count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment submitted and awaiting approval')
    comment_form = CommentForm()

    return render(request,"blog/post_detail.html",
      {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "like_count": like_count,
      },
    )
'''
def like_post(request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

        '''

def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_authenticated:
        if request.user in post.likes.all():
             post.likes.remove(request.user)
             messages.success(request, "You have unliked this post.")
            
        else:
            post.likes.add(request.user)
            messages.success(request, "You liked the post!")
    else:
        messages.error(request, "Please Register to like this post.")
    
    # Instead of redirecting, re-render the post_detail page with the message
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    like_count = post.likes.count()

    comment_form = CommentForm()
    
    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "like_count": like_count,
    })


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))   

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
        )


    def get_context_data(self, **kwargs):
        # Add the category name to the context for display
        context = super().get_context_data(**kwargs)
        context['cat'] = self.kwargs.get('category')
       
        return context
  

   