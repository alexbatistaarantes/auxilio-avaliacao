from dataclasses import field
from rest_framework import serializers

from .models import *

class AssignmentSerializer(serializers.ModelSerializer):
    fields = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    total_points = serializers.FloatField(read_only=True)

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
    assignment_total_points = serializers.FloatField(source='assignment.total_points')
    total_points = serializers.FloatField(read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'

class AnswersSerializer(serializers.ModelSerializer):
    studentId = serializers.CharField(source='submission.studentId')
    submission_image = serializers.ImageField(source='submission.image')
    submission_width = serializers.FloatField(source='submission.width')
    submission_height = serializers.FloatField(source='submission.height')

    field_label = serializers.CharField(source='field.label')
    field_points = serializers.FloatField(source='field.points')
    
    group_name = serializers.CharField(source='group.name', allow_null=True)

    class Meta:
        model = Answer
        fields = '__all__'

class AnswerGroupSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='field.assignment.title', read_only=True)
    
    field_points = serializers.FloatField(source='field.points', read_only=True)
    field_label = serializers.CharField(source='field.label', read_only=True)

    answers = AnswersSerializer(many=True, read_only=True)

    class Meta:
        model = AnswerGroup
        fields = '__all__'
