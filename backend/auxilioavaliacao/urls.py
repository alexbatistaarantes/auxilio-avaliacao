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
    # Rotas para views de função
    path(r'', include(router.urls)),
    path(r'update_answers_group', views.update_answers_group, name='update-answer-group'),
    path('get_assignment_grading_sheet/<int:assignment_id>', views.get_assignment_grading_sheet, name='get-assignment-grading-sheet'),
    path('download_submission_grading/<int:submission_id>', views.download_submission_grading, name='get-submission-grading'),
    path('email_grading/<int:assignment_id>', views.email_grading, name='email-grading'),
    path('get_submissions_from_email/<int:assignment_id>', views.get_submissions_from_email, name='get-submissions-from-email'),
    path('sorters', views.get_sorters, name='get-sorters'),
    path('sort', views.sort_answers, name='sort-answers'),
]
