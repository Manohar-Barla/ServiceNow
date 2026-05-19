from django.urls import path
from . import views

app_name = 'mocktest'

urlpatterns = [
    path('', views.index, name='index'),
    path('summary/', views.summary_view, name='summary'),
    path('start/', views.start_test, name='start'),
    path('submit/', views.submit_test, name='submit'),
]
