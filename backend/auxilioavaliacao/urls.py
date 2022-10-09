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

router.register(r'submissions', views.SubmissionViewSet, basename='submission')
router.register(r'submissions/(?P<submission_id>\d*)/answers', views.SubmissionAnswersViewSet, basename='submissions-answers')

router.register(r'answers', views.AnswerViewSet, basename='answer')

app_name = 'auxilioavaliacao'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_assignment/', views.new_assignment, name='newassignment'),
    path('assignment/<int:assignment_id>/', views.assignment, name='assignment'),
    path('assignment/<int:assignment_id>/field/<int:field_id>/', views.field, name='field'),
    path('assignment/<int:assignment_id>/new_field/', views.new_field, name='newfield'),
    path('assignment/<int:assignment_id>/new_submission/', views.new_submission, name='newsubmission'),
    path('assignment/<int:assignment_id>/submission/<int:submission_id>/', views.submission, name='submission'),

    # REST API
    path(r'api/', include(router.urls)),
]
