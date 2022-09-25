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

    class Meta:
        model = Answer
        fields = '__all__'
