from django.contrib.auth.decorators import login_required

from ..services import *


@login_required
def get_latest(request):
    return get_last_sensor_datum()