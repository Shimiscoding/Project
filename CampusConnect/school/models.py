# models.py
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
import uuid


#Announcements


class Notification(models.Model):
    CATEGORY_CHOICES = (
        ('academics', 'Academics'),
        ('events', 'Events'),
        ('alerts', 'Alerts'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=100, default='No title')
    message = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academics')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
 

    def __str__(self):
        return f"{self.category}: {self.title} - {self.message[:50]}"

    class Meta:
        ordering = ('-created_at',)

class Comment(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.notification.title}"      
    

