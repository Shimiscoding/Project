from django.contrib import admin
from .models import Category, Thread, VotingOption, Comment
# Register your models here.


admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(VotingOption)
admin.site.register(Comment)