from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    
    def __str__(self):
        return " ".join([self.first_name, self.last_name])

class Post(models.Model):
    post_title = models.CharField(max_length=255, unique=True)
    post_subtitle = models.CharField(max_length=255, blank=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_time = models.DateTimeField(auto_now_add=True)
    post_body_md = models.TextField()
    post_body_html = models.TextField()

    def __str__(self):
        return self.post_title
    

class Comment(models.Model):
    comment_page = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_body = models.TextField()

    def __str__(self):
        if len(self.comment_body) < 15:
            return f'By {self.comment_author} | {self.comment_body}'
        else:
            return f'By {self.comment_author} | {self.comment_body[:15]}...'


