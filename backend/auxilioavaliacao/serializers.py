from dataclasses import field
from rest_framework import serializers

from .models import *

class AssignmentSerializer(serializers.ModelSerializer):
    fields = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Assignment        
        fields = '__all__'

class FieldSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    assignment_image = serializers.ImageField(source='assignment.template_image', read_only=True)

    class Meta:
        model = Field
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title')

    class Meta:
        model = Submission
        fields = '__all__'

class AnswersSerializer(serializers.ModelSerializer):
    submission_image = serializers.ImageField(source='submission.image')
    submission_width = serializers.FloatField(source='submission.width')
    submission_height = serializers.FloatField(source='submission.height')
    field_label = serializers.CharField(source='field.label')
    studentId = serializers.CharField(source='submission.studentId')
    group_name = serializers.CharField(source='group.name', allow_null=True)

    class Meta:
        model = Answer
        fields = '__all__'

class AnswerGroupSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = AnswerGroup
        fields = '__all__'
