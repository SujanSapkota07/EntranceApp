from rest_framework import serializers
from .models import Quiz, Question, Option

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["title", "id"]

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields =["option_text", "is_correct"]

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ["question_text", "options"]


