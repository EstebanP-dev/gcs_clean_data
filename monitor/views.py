from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def variables(request):
    return render(request, 'variables/variables.html')

@login_required
def tracking(request):
    return render(request, 'tracking/tracking.html')