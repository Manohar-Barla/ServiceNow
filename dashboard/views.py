from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import TestAttempt

@login_required
def index(request):
    attempts = TestAttempt.objects.filter(user=request.user).order_by('-date')
    stats = attempts.aggregate(
        total_attempts=Count('id'),
        avg_score=Avg('percentage')
    )
    
    # Identify weak domains (simplified: domains where score is low)
    # This would require tracking per-domain score in TestAttempt or a separate model
    # For now, let's just show recent attempts.
    
    return render(request, 'dashboard/dashboard.html', {
        'attempts': attempts,
        'stats': stats
    })
