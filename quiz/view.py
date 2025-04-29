import json
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes   
from rest_framework.permissions import IsAuthenticated  # To make views support HTTP methods like GET, POST etc.
from rest_framework.response import Response           # To send HTTP responses in JSON format
from rest_framework import status     
# Import models and serializers
from .models import Quiz, Question, User, Option    # Our Quiz model
from .serializers import QuizSerializer, QuestionSerializer             # Serializer for Quiz model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate




""" landing page of the quiz app"""
def quiz_landing(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'quiz/landing.html', context)

"""login """
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate inputs
        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect('login')

        # Get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user with that email.")
            return redirect('login')

        # Authenticate using username (Django uses username, not email)
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Replace with your actual dashboard URL name
        else:
            messages.error(request, "Incorrect password.")
            return redirect('login')

    return render(request, 'quiz/login.html')


"""signup """
def signup_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("signup")

        user = User.objects.create_user(
            username=name,
            email=email,
            password=password,
            first_name=name
        )
        return redirect("login")  # Change 'dashboard' to your home page route

    return render(request, "quiz/login.html")

def logout_user(request):
    logout(request)
    return redirect('home')  # Change 'home' to your home page route

def find_quiz(request):
    pass

def create_quiz(request):
    pass


# # here we will create endpoint for our quiz app

# #-- quiz views --#

# # a function to list all the available quizzes
# @api_view(['GET'])  # This view only supports GET requests
# def quiz_list(request):
#     queryset = Quiz.objects.all()
#     serializer = QuizSerializer(queryset, many=True)
#     return Response(serializer.data)



# """ 
# this function now partially shows the qualities of the quiz. 
# makes a user ready for the quiz, shows details like number 
# of questions, created by, etc.
# """

# # a function to show the details of a quiz
# @api_view(['GET'])  
# def quiz_glance(request, pk):
#     try:
#         quiz = Quiz.objects.get(pk=pk)
#     except Quiz.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     # get all the questions from the object "quiz"
#     questions = quiz.questions.all()

#     data = {
#         "id": str(quiz.id),
#         "title": quiz.title,
#         "description": quiz.description,
#         "created_by": quiz.created_by.username,
#         "created_at": quiz.created_at,
#         "number_of_questions": questions.count()
#     }
#     return Response(data)





# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # when quiz_detail is called, it will show all the questions related to that quiz
# def quiz_detail(request, pk):
#     try:
#         quiz = Quiz.objects.get(pk=pk)
#     except Quiz.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     # get all the questions from the object "quiz"
#     questions = quiz.questions.all()
#     serializer = QuestionSerializer(questions, many=True)
#     return Response(serializer.data)




# # # this function is for testing purpose only
# # from django.shortcuts import render
# # from .models import Quiz

# # def quiz_view(request, pk):
# #     # Assuming you have a Quiz model with a related Question model
# #     quiz = Quiz.objects.get(id=pk)
# #     questions = quiz.questions.all()
    
# #     # Prepare question data for passing into the template
# #     questions_data = []
# #     for question in questions:
# #         options = question.options.all()
# #         question_data = {
# #             'question_text': question.question_text,
# #             'options': [{
# #                 # 'letter': option.get_letter(),  # Assuming you have a method to get the option letter (A, B, C, D)
# #                 'option_text': option.option_text,
# #                 'is_correct': option.is_correct,
# #             } for option in options],
# #         }
# #         questions_data.append(question_data)
    
    
# #     # Pass questions data as JSON
# #     return render(request, 'quiz/questions.html', {
# #         'questions_json': json.dumps(questions_data),
# #     })




# """ this is the main function for the quiz app. 
# it will show the landing page of the quiz app."""
# @api_view(['GET', 'POST'])
# def quiz(request):
#     if request.method == 'GET':
#         # This is for "Find" Quiz by code
#         quiz_code = request.query_params.get('code')  
#         # when searces using the code, it will be passed as a query parameter, fetched the uuid for searching
#         if not quiz_code:
#             return Response({'error': 'Quiz code is required'}, status=status.HTTP_400_BAD_REQUEST)
#         # if code not found
        
#         try:
#             quiz = Quiz.objects.get(id=quiz_code)
#             serializer = QuizSerializer(quiz)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Quiz.DoesNotExist:
#             return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     elif request.method == 'POST':
#         # This is for "+ Create New"
#         # We assume the frontend will POST a JSON like { "title": "My Quiz Title" }
#         title = request.data.get('title', 'Untitled Quiz')
#         description = request.data.get('description', '')
#         user = request.user if request.user.is_authenticated else None  # depends if you have login
        
#         quiz = Quiz.objects.create(
#             title=title,
#             description=description,
#             created_by=user
#         )
#         serializer = QuizSerializer(quiz)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)




# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     # username and password are required
#     if not username or not password:
#         return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # authenticate the user
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         token, created = Token.objects.get_or_create(user=user) # created is not required in this case, but is a boolean variable, false if acount is already created.
#         return Response({'token': token.key}, status=status.HTTP_200_OK)
#     else:
#         # if user not found
#         return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def signup(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
    
#     if User.objects.filter(username=username).exists():
#         return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     user = User.objects.create_user(username=username, password=password)
#     token, created = Token.objects.get_or_create(user=user)
#     return Response({'token': token.key}, status=status.HTTP_201_CREATED)




# """
# till here, quiz can be created, viewed, and searched by code.add
# login and signup functionality is done

# now what we have to do is to create a functionality to import or create quiz on the web app and to check the mcqs
# whether they are correct or not.
# we will create a new view for this.
# """
# # views.py

# from django.shortcuts import render, redirect
# from .utils import import_quiz_from_file

# def import_quiz(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         user = request.user  # Assuming user is authenticated
#         import_quiz_from_file(file, user)
#         return redirect('quiz-list')  # or wherever you want
#     return render(request, 'quiz/upload.html')
