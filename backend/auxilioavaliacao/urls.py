from django.urls import path

from . import views

app_name = 'auxilioavaliacao'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_assignment/', views.new_assignment, name='newassignment'),
    path('assignment/<int:assignment_id>/', views.assignment, name='assignment'),
    path('assignment/<int:assignment_id>/field/<int:field_id>/', views.field, name='field'),
    path('assignment/<int:assignment_id>/new_field/', views.new_field, name='newfield'),
]
