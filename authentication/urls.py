from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('logout/', views.logout, name='logout'),
]