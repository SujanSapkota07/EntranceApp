from django.urls import path            # Django's function to define URL patterns
from . import viewset                    # Import our views.py file from the current app

# Define URL patterns for quiz endpoints
urlpatterns = [
    # When visiting /quizzes/, call quiz_list() function
    path('quiz-list/', viewset.quiz_list, name='quiz-list'),

    # When visiting /quizzes/<id>/, call quiz_detail() function with that id
    path('quiz/<uuid:pk>/', viewset.quiz_detail, name='quiz-detail'),
    path('quiz/glance/<uuid:pk>/', viewset.quiz_glance, name='quiz-glance'),

    # landing page or page where we can enter the link or create new quiz
    path('quiz/', viewset.quiz, name = 'quiz'),
     path('login/', viewset.login, name='login'),
    path('signup/', viewset.signup, name='signup'),
]
