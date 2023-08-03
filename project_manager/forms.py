from django import forms
from .models import *

# #Here you can create your forms

class ProjectForm(forms.ModelForm):
    name = models

    class Meta:
        model = Project
        fields = ('title',)

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'})
        }

class ProcessForm(forms.ModelForm):
    name = models

    class Meta:
        model = Process
        fields = ('title',)

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'})
        }


class ActivityForm(forms.ModelForm):
    name = models

    class Meta:
        model = Activity
        fields = ('description',)

        widgets = {
            'description' : forms.Textarea(attrs={'class' : 'form-control'})
        }





