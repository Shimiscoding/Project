from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

from django.db import models

class Parent(models.Model):
    emergency_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self):
        return f"{self.father_name} & {self.mother_name}"

class Teacher(models.Model):
    user = models.OneToOneField('home_auth.CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='teacher_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    date_of_birth = models.DateField()
    teacher_class = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    admission_number = models.CharField(max_length=20)
    teacher_image = models.ImageField(upload_to='Teachers/', blank=True)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name}-{self.last_name}-{self.teacher_id}")
            slug = base_slug
            num = 1
            # Ensure the slug is unique
            while Teacher.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(5)}"  # Appending a random string to ensure uniqueness
                num += 1
            self.slug = slug
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
    
class Meta:
        ordering = ('-joining_date', ) 