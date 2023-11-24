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


class PostLike(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_like', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='liked_post', on_delete=models.CASCADE)

    def __str__(self):
        return f"Post {self.post.id} was liked by {self.user.name}"


class PostDislike(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_disliked', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='disliked_post', on_delete=models.CASCADE)

    def __str__(self):
        return f"Post {self.post.id} was disliked by {self.user.name}"
