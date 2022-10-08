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
        fields = '__all__'

class AnswersSerializer(serializers.ModelSerializer):
    submission_image = serializers.ImageField(source='submission.image')
    submission_width = serializers.FloatField(source='submission.width')
    submission_height = serializers.FloatField(source='submission.height')
    field_label = serializers.CharField(source='field.label')

    class Meta:
        model = Answer
        fields = '__all__'
