from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')
    media_url = models.CharField(blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

