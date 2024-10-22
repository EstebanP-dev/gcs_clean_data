from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from ..services import *

@login_required
def get_data(request, numberOfRows):
    data = get_sensor_data(numberOfRows)

    if data is None:
        return HttpResponse("No hay datos disponibles")
    
    return data