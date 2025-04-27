from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
# a quiz will uniquely identified by its uuid number. there will be no loger sets.



#  a class for user
class User(AbstractUser):
    # everthing is default in the user model

    def __str__(self):
        return self.username    
    


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    # a quiz will have many questions

    def __str__(self):
        return self.title
    



# a class for question
class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # a question will be related to a quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    # question will have many choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text
    

from django.core.exceptions import ValidationError

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Count current options for the question (excluding this one if already exists)
        existing_options = Option.objects.filter(question=self.question).exclude(pk=self.pk)

        # ✅ 1. Check if options already >= 4
        if existing_options.count() >= 4:
            raise ValidationError("A question can have at most 4 options.")

        # ✅ 2. If this option is marked correct, ensure no other correct option exists
        if self.is_correct:
            if existing_options.filter(is_correct=True).exists():
                raise ValidationError("Only one option can be marked as correct.")

    def save(self, *args, **kwargs):
        self.clean()  # run validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.option_text
