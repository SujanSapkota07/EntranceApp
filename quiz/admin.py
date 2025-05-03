from django.contrib import admin

# Register your models here.

from .models import Quiz, Question, Option, User, Category

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(User)
admin.site.register(Category)
