# utils.py

from .models import Quiz, Question, Option




""" 
this function is to import quiz from a file
    the file should be in the following format:
    Question 1  
    A. option 1
    B. option 2
    C. option 3
    D. option 4 
    ANSWER: A
    
    """
def import_quiz_from_file(file_obj, created_by_user):
    content = file_obj.read().decode('utf-8')  
    lines = content.split('\n')
    lines = [line.strip() for line in lines if line.strip()]  # clean empty lines

    # Create Quiz
    quiz = Quiz.objects.create(
        title="Imported Quiz",
        description="Quiz imported from file.",
        created_by=created_by_user
    )

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Handle a question line
        if not (line.startswith('A.') or line.startswith('A)') or line.startswith('A:')) and not line.startswith('ANSWER:'):
            question_text = line
            i += 1

            options = []
            for _ in range(4):
                if i < len(lines):
                    opt_line = lines[i]
                    if opt_line[1] in [')', '.', ':']:
                        option_text = opt_line[2:].strip()
                        options.append(option_text)
                        i += 1
                    else:
                        break
                else:
                    break

            # Get ANSWER
            if i < len(lines) and lines[i].startswith('ANSWER:'):
                answer_line = lines[i]
                correct_letter = answer_line.split(':')[1].strip().upper()
                i += 1
            else:
                correct_letter = None

            # Save Question
            question = Question.objects.create(
                quiz=quiz,
                question_text=question_text
            )

            # Save Options
            letters = ['A', 'B', 'C', 'D']
            for idx, option_text in enumerate(options):
                is_correct = (letters[idx] == correct_letter)
                Option.objects.create(
                    question=question,
                    option_text=option_text,
                    is_correct=is_correct
                )
        else:
            i += 1  # skip bad lines
