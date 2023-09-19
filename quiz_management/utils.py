import random
import string


def generate_password(length=16):
    characters = string.ascii_letters + string.digits
    password = ""
    for _ in range(length):
        random_number = random.randint(0, len(characters) - 1)
        password += characters[random_number]
    return password

def generate_username(email):
    email = email.split('@')
    return email[0]




# def queston(request, quiz_id, type):
#     if request.method == "POST":
#         if type == "mcq":
#             question_form = MCQsQuestionForm(request.POST)
#             if question_form.is_valid():
#                 question_title = question_form.cleaned_data['title']
#                 option1 = question_form.cleaned_data['option_1']
#                 option2 = question_form.cleaned_data['option_2']
#                 option3 = question_form.cleaned_data['option_3']
#                 option4 = question_form.cleaned_data['option_4']
#                 answer = question_form.cleaned_data['answer']
#                 is_public = question_form.cleaned_data['is_public']
#                 marks = question_form.cleaned_data['marks']
#                 print("Following is the Answer ", answer)
#                 print(question_title, option1, option2, option4, option3, answer, is_public, marks)
#                 question_details = {
#                     'question_title': question_title,
#                     'answers': [
#                         {'option1': option1, 'is_correct_answer': 'option1' == answer },
#                         {'option2': option2, 'is_correct_answer': 'option2' == answer },
#                         {'option3': option3, 'is_correct_answer': 'option3' == answer },
#                         {'option4': option4, 'is_correct_answer': 'option4' == answer },
#                         ]
#                     }
#                 question_details_json = json.dumps(question_details)
#                 quiz = Quiz.objects.get(pk=quiz_id)
#                 question = Question.objects.create(question_details=question_details_json, marks=marks, is_public=is_public)
#                 question.quiz.add(quiz)
#                 question.save()
#                 return HttpResponseRedirect('/quiz_management/question/1/mcq/')
            
#             return render(request, 'quiz_management/add_question.html', {'question_form': question_form, 
#                                                                  'question_type': "mcqs",
#                                                                  })
        
#     else:      
#         if type == "mcq":
#             question_form = MCQsQuestionForm()
#             question_type = "mcqs"
#             print("working")
#         elif type == "subjective":
#             question_form = "This is Subjective"
#         else:
#             question_form = "This is Binary Choice"
        
#         return render(request, 'quiz_management/add_question.html', {'question_form': question_form, 
#                                                                  'question_type': question_type
#                                                                  })
