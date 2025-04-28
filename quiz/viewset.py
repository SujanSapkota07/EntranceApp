# Import the necessary decorators and functions from DRF
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

# bulk upload from provious quiz project

# viewset.py

# @api_view(['GET'])
@permission_classes([IsAuthenticated])
def import_quiz(request):
    """
    Expects a file upload (multipart/form-data) under 'file'.
    The .txt must have MCQ blocks like:
       Question text…
       A. option1
       B. option2
       C. option3
       D. option4

       ANSWER: C

    The filename (without .txt) becomes the Quiz.title.
    """
    # 1️⃣ Grab the uploaded file
    if request.method == 'GET':
        uploaded = request.FILES.get('file')
        if not uploaded or not uploaded.name.endswith('.txt'):
            return Response(
                {'error': 'A .txt file is required under “file”.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Create the Quiz

        quiz = Quiz.objects.create(
            title=f'unknown file by {request.user.username}',
            description='',              
            created_by=request.user
        )

        # 3️⃣ Read and normalize lines
        content = uploaded.read().decode('utf-8')
        lines = [ln.strip() for ln in content.splitlines()]

        # 4️⃣ Split into blocks (one block = one question + options + ANSWER)
        blocks, current = [], []
        for ln in lines:
            if ln == '' and current:
                blocks.append(current)
                current = []
            elif ln != '':
                current.append(ln)
        if current:
            blocks.append(current)

        # 5️⃣ Parse each block
        for blk in blocks:
            # a) Find and remove the ANSWER line
            answer_line = next((l for l in blk if l.upper().startswith('ANSWER')), None)
            if not answer_line:
                # skip malformed block
                continue
            correct_letter = answer_line.split(':', 1)[1].strip().upper()
            blk = [l for l in blk if not l.upper().startswith('ANSWER')]

            # b) First line is the question text
            question_text = blk[0]
            q = Question.objects.create(quiz=quiz, question_text=question_text)

            # c) Next lines starting with A., B., C., D. are options
            for opt_line in blk[1:]:
                if len(opt_line) < 2 or opt_line[1] != '.':
                    continue
                letter = opt_line[0].upper()
                text = opt_line[2:].strip()
                is_correct = (letter == correct_letter)
                Option.objects.create(
                    question=q,
                    option_text=text,
                    is_correct=is_correct
                )

        # 6️⃣ Return the newly created quiz
        # return Response(
        #     {'quiz_id': str(quiz.id), 'title': quiz.title},
        #     status=status.HTTP_201_CREATED
        # )
        return render(request, 'quiz/index.html', {'quiz': quiz})
