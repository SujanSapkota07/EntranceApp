# Import the necessary decorators and functions from DRF
from rest_framework.decorators import api_view         # To make views support HTTP methods like GET, POST etc.
from rest_framework.response import Response           # To send HTTP responses in JSON format
from rest_framework import status                      # Provides readable HTTP status codes like 404, 200, etc.

# Import models and serializers
from .models import Quiz                               # Our Quiz model
from .serializers import QuizSerializer                # Serializer for Quiz model



# here we will create endpoint for our quiz app

#-- quiz views --#

# a function to list all the available quizzes
@api_view(['GET'])  # This view only supports GET requests
def quiz_list(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)


def quiz_detail(request, pk):
    try:
        # Try to get the quiz object by primary key (id)
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        # If the object doesn't exist, return 404 NOT FOUND
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # If request is GET, serialize the quiz and return it
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # If request is PUT, update the quiz with new data
        serializer = QuizSerializer(quiz, data=request.data)
        # Validate the new data
        if serializer.is_valid():
            # Save the updated quiz object
            serializer.save()
            # Return updated data
            return Response(serializer.data)
        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # If request is DELETE, delete the quiz from the database
        quiz.delete()
        # Return 204 NO CONTENT to indicate successful deletion
        return Response(status=status.HTTP_204_NO_CONTENT)
