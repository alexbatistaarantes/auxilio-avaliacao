from django.forms import ModelForm, IntegerField

from .models import *

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'template_image']

class FieldForm(ModelForm):

    class Meta:
        model = Field
        exclude = ('assignment', 'pctX1', 'pctY1', 'pctX2', 'pctY2')

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['studentId', 'image']
