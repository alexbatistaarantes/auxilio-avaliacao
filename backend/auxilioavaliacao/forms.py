from django.forms import ModelForm, IntegerField

from .models import *

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'template_image']

class FieldForm(ModelForm):

    class Meta:
        model = Field
        fields = ['label', 'x', 'y', 'width', 'height']

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['studentId', 'image']
