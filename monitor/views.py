from django.shortcuts import render
from django.contrib.auth.decorators import login_required

context = {
    'update_interval': 1000,  # Intervalo en milisegundos (1000 ms = 1 segundo)
}

@login_required
def variables(request):
    return render(request, 'variables/variables.html', context)

@login_required
def tracking(request):
    return render(request, 'tracking/tracking.html', context)