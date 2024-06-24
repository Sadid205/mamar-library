from django import forms 
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        placeholders = {
            'name':'Enter Your Name',
            'body':'Enter Your Review',
        }
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'shadow-2xl p-3 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full'
                ),
                'placeholder':placeholders[field]
            })