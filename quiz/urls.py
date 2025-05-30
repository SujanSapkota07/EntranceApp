from django.urls import path            # Django's function to define URL patterns
from . import view              
# Define URL patterns for quiz endpoints
urlpatterns = [
    path ('', view.quiz_landing, name='home'),
    path('login/', view.login_user, name='login'),
    path('logout/', view.logout_user, name='logout'),
    path('signup/', view.signup_user, name='signup'),
    path('find_quiz/', view.find_quiz, name='find_quiz'),
    path('create_quiz/', view.create_quiz, name='create_quiz'),
    path('upload/', view.upload_quiz, name='upload_quiz'),
    path('mydashboard/', view.mydashboard, name='mydashboard'),
    path('quiz/view/<uuid:quiz_id>/', view.view_quiz, name='view_quiz'),
    path('quiz/edit/<uuid:quiz_id>/', view.edit_quiz, name='edit_quiz'),
    path('save_quiz/<uuid:quiz_id>/', view.save_quiz, name='save_quiz'),
]

#     # When visiting /quizzes/, call quiz_list() function
#     path('quiz-list/', viewset.quiz_list, name='quiz-list'),

#     # When visiting /quizzes/<id>/, call quiz_detail() function with that id
#     path('quiz/<uuid:pk>/', viewset.quiz_detail, name='quiz-detail'),
#     # path('quiz_view/<uuid:pk>/', viewset.quiz_view, name='quiz-detail'),
#     path('quiz/glance/<uuid:pk>/', viewset.quiz_glance, name='quiz-glance'),

#     # landing page or page where we can enter the link or create new quiz
#     path('quiz/', viewset.quiz, name = 'quiz'),
#     path('login/', viewset.login, name='login'),
#     path('signup/', viewset.signup, name='signup'),

# path('import_quiz/', viewset.import_quiz, name='import-quiz'),











# BY CHATGPT
    # path('upload/', viewset.upload_mcqs, name='upload_mcqs'),
    # path('play/', viewset.play_mcqs, name='play_mcqs'),

