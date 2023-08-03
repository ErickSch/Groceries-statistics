from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def statistics(request):
    
    return render(request, 'lists_statistics/statistics.html')