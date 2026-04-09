from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=600)
    content = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_favourite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title
    
    
