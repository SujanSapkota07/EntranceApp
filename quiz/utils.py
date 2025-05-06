import re

from django.template.defaultfilters import title

from .models import Quiz, Question, Option

from .models import Question

def get_questions_by_quiz(quiz_id):
    return Question.objects.filter(quiz_id=quiz_id)



def import_quiz_from_file(file_obj, created_by_user):
    print("Importing quiz from file...")
    content = file_obj.read().decode('utf-8')
    lines = content.strip().split('\n')

    # Clean lines
    lines = [line.strip() for line in lines if line.strip()]
    filename = file_obj.name
    # Create the quiz
    quiz = Quiz.objects.create(
        title=filename[:15],
        description="Quiz imported from file.",
        created_by=created_by_user
    )
    print(f"Created quiz: {quiz.title}, ID: {quiz.id}")

    i = 0
    while i < len(lines):
        question_text = lines[i]
        i += 1

        # Get 4 options
        options = []
        while i < len(lines) and len(options) < 4:
            match = re.match(r'([A-D])[.)-]?\s+(.*)', lines[i])
            if match:
                options.append((match.group(1).strip().upper(), match.group(2).strip()))
                i += 1
            else:
                break

        # Get the correct answer
        correct_letter = None
        if i < len(lines) and lines[i].startswith('ANSWER:'):
            correct_letter = lines[i].split(':')[1].strip().upper()
            i += 1

        # Save question
        question = Question.objects.create(
            quiz=quiz,
            question_text=question_text
        )

        # Save options
        for opt_letter, opt_text in options:
            is_correct = (opt_letter == correct_letter)
            Option.objects.create(
                question=question,
                option_text=opt_text,
                is_correct=is_correct
            )

