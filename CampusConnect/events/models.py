from django.db import models
from django.conf import settings
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Reverse the URL for the event detail view (make sure to define this URL in your urls.py)
        return reverse('event_detail', kwargs={'pk': self.pk})


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} RSVP for {self.event.title}"

    class Meta:
        unique_together = ('event', 'user')  # Ensures each user can RSVP only once per event
