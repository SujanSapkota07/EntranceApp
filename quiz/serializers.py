from rest_framework import serializers
from .models import Quiz, Question, Option

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'description']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['question','option_text', 'is_correct']
        read_only_fields = ['id', 'created_at', 'updated_at']