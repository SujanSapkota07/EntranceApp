# Import the necessary decorators and functions from DRF
from rest_framework.decorators import api_view         # To make views support HTTP methods like GET, POST etc.
from rest_framework.response import Response           # To send HTTP responses in JSON format
from rest_framework import status                      # Provides readable HTTP status codes like 404, 200, etc.

# Import models and serializers
from .models import Quiz, Question               # Our Quiz model
from .serializers import QuizSerializer, QuestionSerializer             # Serializer for Quiz model



# here we will create endpoint for our quiz app

#-- quiz views --#

# a function to list all the available quizzes
@api_view(['GET'])  # This view only supports GET requests
def quiz_list(request):
    queryset = Quiz.objects.all()
    serializer = QuizSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(['GET'])
# when quiz_detail is called, it will show all the questions related to that quiz
def quiz_detail(request, pk):
    print(1)
    try:
        quiz = Quiz.objects.get(pk=pk)
        print(quiz)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get all the questions from the object "quiz"
    questions = quiz.questions.all()
    print(questions)
    print(1)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)
    