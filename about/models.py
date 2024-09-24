from django.db import models

# Create your models here.
class About(models.Model):
    """
    Stores "about the site" text
    """
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title