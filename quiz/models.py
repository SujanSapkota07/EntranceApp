from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError


# Create your models here.
# a quiz will uniquely identified by its uuid number. there will be no loger sets.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


#  a class for user
class User(AbstractUser):
    # everthing is default in the user model

    def __str__(self):
        return self.username


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='quiz/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    # add time limit to play quiz
    time_limit = models.IntegerField(default=0)  # in minutes

    # a quiz will have many questions

    def __str__(self):
        return self.title


# a class for question
class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # a question will be related to a quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    # a
    # question will have many choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super(Question, self).save(*args, **kwargs)
        # Count current options for the question (excluding this one if already exists)
        if self.options.all().count() > 4:
            raise ValidationError("A question can have at most 4 options.")

        if self.options.filter(is_correct=True).count() > 1:
            # ✅ 2. If this option is marked correct, ensure no other correct option exists
            raise ValidationError("Only one option can be marked as correct.")
        # ✅ 3. Ensure at least one correct option exists
        # if not self.is_correct and existing_options.filter(is_correct=True).count() == 0:
        #     raise ValidationError("There must be at least one correct option for the question.")
        if not self.options.filter(is_correct=True).count() == 1:
            raise ValidationError("At least one option must be marked as correct.")

    def __str__(self):
        return self.question_text


class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    image = models.ImageField(upload_to='options/', blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def clean(self):
    #     # Count current options for the question (excluding this one if already exists)
    #     existing_options = Option.objects.filter(question=self.question).exclude(pk=self.pk)
    #     print(existing_options)
    #
    #     # ✅ 1. Check if options already >= 4
    #     if existing_options.count() >= 4:
    #         raise ValidationError("A question can have at most 4 options.")
    #
    #     # ✅ 2. If this option is marked correct, ensure no other correct option exists
    #     if self.is_correct:
    #         if existing_options.filter(is_correct=True).exists():
    #             # raise ValidationError("Only one option can be marked as correct.")
    #             pass
    #     # ✅ 3. Ensure at least one correct option exists
    #     # if not self.is_correct and existing_options.filter(is_correct=True).count() == 0:
    #     #     raise ValidationError("There must be at least one correct option for the question.")
    #
    #     if not self.is_correct:
    #         # Check if there are any existing correct options
    #         correct_option_count = existing_options.filter(is_correct=True).count()
    #         if self.is_correct:
    #             correct_option_count += 1  # Include this option if it's marked correct
    #         if existing_options.count() >= 3:
    #             if correct_option_count == 0:
    #                 print("here")
    #                 # raise ValidationError("At least one option must be marked as correct.")

    def save(self, *args, **kwargs):
        self.clean()  # run validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.option_text
