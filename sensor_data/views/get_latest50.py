from django.contrib.auth.decorators import login_required

from ..services import *


@login_required
def get_latest50(request):
    return get_last_50_sensor_data()