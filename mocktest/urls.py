from django.urls import path
from . import views

app_name = 'mocktest'

urlpatterns = [
    path('', views.index, name='index'),
    path('summary/', views.summary_view, name='summary'),
    path('start/', views.start_test, name='start'),
    path('submit/', views.submit_test, name='submit'),
    path('api/get_question/', views.get_question_api, name='api_get_question'),
]
