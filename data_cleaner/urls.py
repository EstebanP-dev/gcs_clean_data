from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('clean-data/', views.clean_data_view),  
]