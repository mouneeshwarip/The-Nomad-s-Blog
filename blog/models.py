from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))

class Category(models.Model):
    # Defines the category of posts with a unique name for each category
    name = models.CharField(max_length=100, unique=True)

    class Meta:
       # Defines the plural name for display in the admin panel and orders categories alphabetically by name
        verbose_name_plural = "Categories"  
        ordering = ['name']   

    def __str__(self):
        return self.name

class Post(models.Model):
    # Stores all the blog posts with details such as title, content, author, and status
    title=models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt = models.CharField(max_length=200, blank=True) 
    featured_image = models.ImageField(upload_to='images/', blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        # Orders posts by creation date, with the oldest first
        ordering = ["created_on"]

    def __str__(self):
        return f"The title of this post is {self.title} by {self.author}"    

class Comment(models.Model):
    # Stores all the comments associated with a specific post and user
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders comments by creation date, with the newest comments first
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.user}"   

class Like(models.Model):
    # Tracks likes for posts, can be associated with a registered user or an anonymous session
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  #For anonymous likes
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders likes by the date they were made, with the most recent first
        ordering = ["-liked_on"]

    def __str__(self):
        return f"{self.user or 'Anonymous'} liked {self.post.title}"     

class Share(models.Model):
    # Tracks shares for posts, can be associated with a registered user or an anonymous session
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  #For anonymous shares
    shared_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders shares by the date they were made, with the most recent first
        ordering = ["-shared_on"]

    def __str__(self):
        return f"{self.user or 'Anonymous'} shared {self.post.title}"           
