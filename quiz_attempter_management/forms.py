from django import forms
from .models import Discussion, Comment


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['subject', 'details']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter details'})
        }

        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['comment']
        