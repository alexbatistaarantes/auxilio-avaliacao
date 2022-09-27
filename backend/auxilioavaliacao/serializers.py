from rest_framework import serializers

from .models import *

class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment        
        fields = '__all__'

class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = ['studentId', 'image', 'answers']

class AnswersSerializer(serializers.ModelSerializer):
    submission_image = serializers.ImageField(source='submission.image')
    field_label = serializers.CharField(source='field.label')

    class Meta:
        model = Answer
        fields = '__all__'
