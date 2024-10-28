from django.urls import path

from . import views

app_name = 'monitor'

urlpatterns = [
    path('variables/', views.variables, name='variables'),
    path('statistics/', views.statistics, name='statistics'),
    path('tracking/', views.tracking, name='tracking')
    
]