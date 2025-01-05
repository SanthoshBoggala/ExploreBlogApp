from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

class EditRequest(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        GIVEN = 'given', 'Given'
        CLOSED = 'closed', 'Closed'
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_edit_requests')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    requested = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_edit_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)