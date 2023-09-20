from django import forms
from .models import Quiz, QuizAttempter, Question, Announcement


class QuizAttempterForm(forms.ModelForm):
    class Meta:
        model = QuizAttempter
        fields = ['email']
        labels = {'email': "Attempter Email Address"}


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'category', 'start_time', 'end_time']
        labels = {
            'title': "Quiz Title", 'category': 'Quiz Category',
            'start_time': 'Start Time', 'end_time': 'End Time'
                }
        widgets = {
            'start_time': forms.DateInput(
                attrs={'type': 'datetime-local'}
            ),
            'end_time':forms.DateInput(
                attrs={'type': 'datetime-local'}
            ),
        }      
        

class MCQsQuestionForm(forms.Form):
    title = forms.CharField(label='Question Title', max_length=200)
    option_1 = forms.CharField(label='Option 1', max_length=200)
    option_2 = forms.CharField(label='Option 2', max_length=200)
    option_3 = forms.CharField(label='Option 3', max_length=200)
    option_4 = forms.CharField(label='Option 4', max_length=200)
    answer = forms.ChoiceField(
        label='Correct Answer',
        choices=(
            ('option1', 'Option 1'),
            ('option2', 'Option 2'),
            ('option3', 'Option 3'),
            ('option4', 'Option 4'),
        ),
    )
    marks = forms.DecimalField(label='Marks')
    is_public = forms.BooleanField(required=False)
    

class SubjectiveQuestionForm(forms.Form):
    title = forms.CharField(label="Question Title", max_length=200)
    answer = forms.CharField(label="Correct Answer", max_length=400)
    marks = forms.DecimalField(label="Marks")
    is_public = forms.BooleanField(required=False)
    

# class BooleanQuestionForm(forms.Form):
#     title = forms.CharField(label="Queston Title", max_length=200)
#     answer = forms.ChoiceField(
#         label="Answer",
#         choices=[("true", "True"), ("false", "False")],
#         widget=forms.RadioSelect,
#         required=True,
#     )
   

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['subject', 'details']
        # widget = {
        #     'preparation_material': forms.FileField(required=False)
        # }
        