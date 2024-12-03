from django.db import models
from django.conf import settings

# Define category choices
CATEGORY_CHOICES = (
    ('academics', 'Academics'),
    ('events', 'Events'),
    ('alerts', 'Alerts'),
)

class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Uses custom user model
    created_at = models.DateTimeField(auto_now_add=True)
    enable_voting = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_threads', blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-created_at',)

class VotingOption(models.Model):
    thread = models.ForeignKey(Thread, related_name='voting_options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)  # Track number of votes for each option

    def __str__(self):
        return self.option_text

class Comment(models.Model):
    thread = models.ForeignKey(Thread, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE)  # Uses custom user model
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.thread.title}"

