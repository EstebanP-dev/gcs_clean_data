from django.contrib.auth.decorators import login_required

from ..services import *


@login_required
def data_cleaned(request):
    return get_all_sesor_data_cleaned()