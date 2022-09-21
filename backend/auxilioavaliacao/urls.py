from django.urls import path

from . import views

app_name = 'auxilioavaliacao'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_image/', views.new_image, name='newimage'),
    path('image/<int:image_id>/', views.image, name='image'),
    path('image/<int:image_id>/region/<int:region_id>/', views.region, name='region'),
    path('image/<int:image_id>/new_region/', views.new_region, name='newregion'),
]
