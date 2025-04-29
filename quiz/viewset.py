# Import the necessary decorators and functions from DRF
import json
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes   
from rest_framework.permissions import IsAuthenticated  # To make views support HTTP methods like GET, POST etc.
from rest_framework.response import Response           # To send HTTP responses in JSON format
from rest_framework import status     
                 # Provides readable HTTP status codes like 404, 200, etc.

# Import models and serializers
from .models import Quiz, Question, User, Option    # Our Quiz model
from .serializers import QuizSerializer, QuestionSerializer             # Serializer for Quiz model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate



# here we will create endpoint for our quiz app

#-- quiz views --#

# a function to list all the available quizzes
@api_view(['GET'])  # This view only supports GET requests
def quiz_list(request):
    queryset = Quiz.objects.all()
    serializer = QuizSerializer(queryset, many=True)
    return Response(serializer.data)



""" 
this function now partially shows the qualities of the quiz. 
makes a user ready for the quiz, shows details like number 
of questions, created by, etc.
"""

# a function to show the details of a quiz
@api_view(['GET'])  
def quiz_glance(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get all the questions from the object "quiz"
    questions = quiz.questions.all()

    data = {
        "id": str(quiz.id),
        "title": quiz.title,
        "description": quiz.description,
        "created_by": quiz.created_by.username,
        "created_at": quiz.created_at,
        "number_of_questions": questions.count()
    }
    return Response(data)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
# when quiz_detail is called, it will show all the questions related to that quiz
def quiz_detail(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get all the questions from the object "quiz"
    questions = quiz.questions.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)




# # this function is for testing purpose only
# from django.shortcuts import render
# from .models import Quiz

# def quiz_view(request, pk):
#     # Assuming you have a Quiz model with a related Question model
#     quiz = Quiz.objects.get(id=pk)
#     questions = quiz.questions.all()
    
#     # Prepare question data for passing into the template
#     questions_data = []
#     for question in questions:
#         options = question.options.all()
#         question_data = {
#             'question_text': question.question_text,
#             'options': [{
#                 # 'letter': option.get_letter(),  # Assuming you have a method to get the option letter (A, B, C, D)
#                 'option_text': option.option_text,
#                 'is_correct': option.is_correct,
#             } for option in options],
#         }
#         questions_data.append(question_data)
    
    
#     # Pass questions data as JSON
#     return render(request, 'quiz/questions.html', {
#         'questions_json': json.dumps(questions_data),
#     })




""" this is the main function for the quiz app. 
it will show the landing page of the quiz app."""
@api_view(['GET', 'POST'])
def quiz(request):
    if request.method == 'GET':
        # This is for "Find" Quiz by code
        quiz_code = request.query_params.get('code')  
        # when searces using the code, it will be passed as a query parameter, fetched the uuid for searching
        if not quiz_code:
            return Response({'error': 'Quiz code is required'}, status=status.HTTP_400_BAD_REQUEST)
        # if code not found
        
        try:
            quiz = Quiz.objects.get(id=quiz_code)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        # This is for "+ Create New"
        # We assume the frontend will POST a JSON like { "title": "My Quiz Title" }
        title = request.data.get('title', 'Untitled Quiz')
        description = request.data.get('description', '')
        user = request.user if request.user.is_authenticated else None  # depends if you have login
        
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            created_by=user
        )
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # username and password are required
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user) # created is not required in this case, but is a boolean variable, false if acount is already created.
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        # if user not found
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)




"""
till here, quiz can be created, viewed, and searched by code.add
login and signup functionality is done

now what we have to do is to create a functionality to import or create quiz on the web app and to check the mcqs
whether they are correct or not.
we will create a new view for this.
"""
from django.shortcuts import render, redirect
from .models import Quiz, Question, Option
import os
from django.contrib.auth.decorators import login_required

@login_required
def import_quiz(request):
    """
    Uploads a text file containing MCQs and saves the Quiz, Questions, and Options into the database.
    """
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file or not uploaded_file.name.endswith('.txt'):
            return render(request, 'quiz/error.html', {'error': 'Please upload a .txt file only.'})
        
        # Create the Quiz
        quiz_title = os.path.splitext(uploaded_file.name)[0]
        quiz = Quiz.objects.create(
            title=quiz_title,
            description='Imported Quiz',
            created_by=request.user
        )

        # Read and process the file
        content = uploaded_file.read().decode('utf-8')
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        # Split into blocks
        blocks = []
        current_block = []

        for line in lines:
            if line.upper().startswith('ANSWER'):
                current_block.append(line)
                blocks.append(current_block)
                current_block = []
            else:
                current_block.append(line)
        
        if current_block:
            blocks.append(current_block)

        # Parse each block
        for block in blocks:
            if len(block) < 6:
                continue  # must have at least 1 question, 4 options, 1 answer

            question_text = block[0]

            option_lines = block[1:-1]  # all lines between question and answer
            answer_line = block[-1]

            if len(option_lines) != 4:
                continue  # Skip if not exactly 4 options

            correct_letter = answer_line.split(':', 1)[1].strip().upper()

            # Create the Question
            question = Question.objects.create(
                quiz=quiz,
                question_text=question_text,
            )

            for opt_line in option_lines:
                # Handle different formats like A), A., A:
                if len(opt_line) < 2:
                    continue

                letter = opt_line[0].upper()
                if opt_line[1] in [')', '.', ':']:
                    option_text = opt_line[2:].strip()
                else:
                    continue  # Invalid format, skip

                if not option_text:
                    continue  # Skip if option text empty

                # Create the Option
                Option.objects.create(
                    question=question,
                    option_text=option_text,
                    is_correct=(letter == correct_letter)
                )

        return redirect('quiz-list')  # after successful upload

    return render(request, 'quiz/upload.html')

