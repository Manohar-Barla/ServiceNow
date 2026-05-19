from django.shortcuts import render
from .models import Resource

def index(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'resources/resources.html', {'resources': resources})
