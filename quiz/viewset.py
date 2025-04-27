# Import the necessary decorators and functions from DRF
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

