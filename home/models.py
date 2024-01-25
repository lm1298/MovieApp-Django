from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tv_id = models.IntegerField(blank=True, null=True)

class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField(null=True)  # Adjust this field based on your Movie model
    tv_show_id = models.IntegerField(null=True)  # Adjust this field based on your TV Show model

    def __str__(self):
        return f"{self.user.username}'s Watchlist Item"        