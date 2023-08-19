from django import forms

from .models import Comment

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )
        widgets = {'comment': forms.TextInput(attrs={
            'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }