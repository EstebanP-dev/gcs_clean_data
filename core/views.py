from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'statistics/indicators.html')

@login_required
def products(request):
    return render(request, 'core/products.html')