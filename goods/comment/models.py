from django.db import models
from django.contrib.auth.models import User

from item.models import Item

class Comment(models.Model):
    posted_py = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    belonging_item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.posted_py.username} - {self.belonging_item.name}'