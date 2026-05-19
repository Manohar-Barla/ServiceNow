from django.urls import path
from . import views

app_name = 'question_manager'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_question, name='add_question'),
    path('edit/<int:pk>/', views.edit_question, name='edit_question'),
    path('delete/<int:pk>/', views.delete_question, name='delete_question'),
    path('preview/<int:pk>/', views.preview_question, name='preview_question'),
    path('upload/', views.bulk_upload, name='bulk_upload'),
]
