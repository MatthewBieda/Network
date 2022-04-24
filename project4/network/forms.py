from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django import forms
from .models import Post

class NewPost(ModelForm):
    
    class Meta:
        model = Post
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control w-25'})
        }

        labels = {
            'content': ''
        }