from django.urls import path
from . import views

app_name = 'syllabus'

urlpatterns = [
    path('', views.index, name='index'),
    path('domain/<int:domain_id>/', views.domain_detail, name='domain_detail'),
]
