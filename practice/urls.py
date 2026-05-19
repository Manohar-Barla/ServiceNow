from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('', views.index, name='index'),
    path('topic/<str:topic_name>/', views.practice_by_topic, name='practice_by_topic'),
    path('quiz/<str:topic_name>/', views.quiz_view, name='quiz'),
]
