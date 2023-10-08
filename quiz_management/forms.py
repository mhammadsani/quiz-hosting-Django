from django import forms
from .models import Quiz, QuizAttempter, Question, Announcement


class QuizAttempterForm(forms.ModelForm):
    class Meta:
        model = QuizAttempter
        fields = ['email']
        labels = {'email': "Attempter Email Address"}
        

class QuizAttempterForm(forms.ModelForm):
    class Meta:
        model = QuizAttempter
        fields = ['email']
        labels = {'email': "Attempter Email Address"}

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'})
    )


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
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'end_time':forms.DateInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }      
        

# class MCQsQuestionForm(forms.Form):
#     title = forms.CharField(label='Question Title', max_length=200)
#     option_1 = forms.CharField(label='Option 1', max_length=200)
#     option_2 = forms.CharField(label='Option 2', max_length=200)
#     option_3 = forms.CharField(label='Option 3', max_length=200)
#     option_4 = forms.CharField(label='Option 4', max_length=200)
#     answer = forms.ChoiceField(
#         label='Correct Answer',
#         choices=(
#             ('option1', 'Option 1'),
#             ('option2', 'Option 2'),
#             ('option3', 'Option 3'),
#             ('option4', 'Option 4'),
#         ),
#     )
#     marks = forms.DecimalField(label='Marks')
#     is_public = forms.BooleanField(required=False)


class MCQsQuestionForm(forms.Form):
    title = forms.CharField(
        label='Question Title',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    option_1 = forms.CharField(
        label='Option 1',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    option_2 = forms.CharField(
        label='Option 2',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    option_3 = forms.CharField(
        label='Option 3',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    option_4 = forms.CharField(
        label='Option 4',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    answer = forms.ChoiceField(
        label='Correct Answer',
        choices=(
            ('option1', 'Option 1'),
            ('option2', 'Option 2'),
            ('option3', 'Option 3'),
            ('option4', 'Option 4'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    marks = forms.DecimalField(
        label='Marks',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    is_public = forms.BooleanField(
        required=False
    )

    

# class SubjectiveQuestionForm(forms.Form):
#     title = forms.CharField(label="Question Title", max_length=200)
#     answer = forms.CharField(label="Correct Answer", max_length=400)
#     marks = forms.DecimalField(label="Marks")
#     is_public = forms.BooleanField(required=False)


class SubjectiveQuestionForm(forms.Form):
    title = forms.CharField(
        label="Question Title",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    answer = forms.CharField(
        label="Correct Answer",
        max_length=400,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    marks = forms.DecimalField(
        label="Marks",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    is_public = forms.BooleanField(
        required=False
    )

    
class BooleanQuestionForm(forms.Form):
    title = forms.CharField(label="Question Title", max_length=200, required=True)
    CORRECT_ANSWER_CHOICES = (
        ('true', 'True'),
        ('false', 'False')
    )
    answer = forms.ChoiceField(
        label='Correct Answer',
        widget=forms.RadioSelect,
        choices=CORRECT_ANSWER_CHOICES, 
        required=True
    )
    marks = forms.DecimalField(label="Marks")
    is_public = forms.BooleanField(label="Is Public", required=False)


# class BooleanQuestionForm(forms.Form):
#     title = forms.CharField(label="Queston Title", max_length=200)
#     answer = forms.ChoiceField(
#         label="Answer",
#         choices=[("true", "True"), ("false", "False")],
#         widget=forms.RadioSelect,
#         required=True,
#     )


# class BooleanQuestionForm(forms.Form):
#     title = forms.CharField(
#         label="Question Title",
#         max_length=200,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     is_true = forms.BooleanField(
#         label="True",
#         required=True,
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
#     )
#     marks = forms.DecimalField(
#         label="Marks",
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#     )
#     is_public = forms.BooleanField(
#         required=False
#     )

   

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['subject', 'details']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        