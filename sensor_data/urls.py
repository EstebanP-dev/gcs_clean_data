from django.urls import path

from . import views
from . import constants

app_name = 'sensor_data'

urlpatterns = [
    path(constants.GET_LATEST, views.get_latest, name='get_latest'),
    path(constants.CREATE_DATA, views.create_data, name='create_data'),
]