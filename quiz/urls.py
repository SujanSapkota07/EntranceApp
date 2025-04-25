from django.urls import path            # Django's function to define URL patterns
from . import views                    # Import our views.py file from the current app

# Define URL patterns for quiz endpoints
urlpatterns = [
    # When visiting /quizzes/, call quiz_list() function
    path('quizzes/', views.quiz_list, name='quiz-list'),

    # When visiting /quizzes/<id>/, call quiz_detail() function with that id
    path('quizzes/<int:pk>/', views.quiz_detail, name='quiz-detail'),
]
