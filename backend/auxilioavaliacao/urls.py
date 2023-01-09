from django.urls import path, include
from rest_framework import routers

from . import views

# REST API
router = routers.DefaultRouter()
router.register(r'assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'assignments/(?P<assignment_id>\d*)/fields', views.AssignmentFieldsViewSet, basename='assignment-fields')
router.register(r'assignments/(?P<assignment_id>\d*)/submissions', views.AssignmentSubmissionsViewSet, basename='assignment-submissions')

router.register(r'fields', views.FieldViewSet, basename='field')
router.register(r'fields/(?P<field_id>\d*)/answers', views.FieldAnswersViewSet, basename='field-answers')
router.register(r'fields/(?P<field_id>\d*)/groups', views.FieldAnswerGroupsViewSet, basename='field-answergroups')

router.register(r'submissions', views.SubmissionViewSet, basename='submission')
router.register(r'submissions/(?P<submission_id>\d*)/answers', views.SubmissionAnswersViewSet, basename='submissions-answers')

router.register(r'groups', views.AnswerGroupViewSet, basename='groups')

router.register(r'answers', views.AnswerViewSet, basename='answer')

app_name = 'auxilioavaliacao'
urlpatterns = [
    # REST API
    path(r'api/', include(router.urls)),
    path(r'api/update_answers_group', views.update_answers_group, name='update-answer-group'),
    path('api/get_assignment_grading_sheet/<int:assignment_id>', views.get_assignment_grading_sheet, name='get-assignment-grading-sheet'),
    path('api/download_submission_grading/<int:submission_id>', views.download_submission_grading, name='get-submission-grading')
]
