from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=3)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt = models.CharField(max_length=200, blank=True) 
    #featured_image = models.ImageField(upload_to='images/', blank=True, null=True)
    featured_image = CloudinaryField('image', blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name="liked_posts")

    class Meta:
        # Orders posts by creation date, with the oldest first
        ordering = ["created_on"]

    def __str__(self):
        return f"The title of this post is {self.title} by {self.author}"    

class Comment(models.Model):
    # Stores all the comments associated with a specific post and user
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders comments by creation date, with the newest comments first
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"   

class Like(models.Model):
    # Tracks likes for posts, can be associated with a registered user or an anonymous session
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_set')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  #For anonymous likes
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders likes by the date they were made, with the most recent first
        ordering = ["-liked_on"]

    def __str__(self):
        return f"{self.author or 'Anonymous'} liked {self.post.title}"     

