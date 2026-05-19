from django.shortcuts import render, get_object_or_404
from .models import Domain, Topic

def index(request):
    domains = Domain.objects.all().order_by('name')
    return render(request, 'syllabus/syllabus.html', {'domains': domains})

def domain_detail(request, domain_id):
    domain = get_object_or_404(Domain, pk=domain_id)
    topics = domain.topics.all()
    return render(request, 'syllabus/domain_detail.html', {'domain': domain, 'topics': topics})
