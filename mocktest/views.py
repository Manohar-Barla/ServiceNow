from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from question_manager.models import Question
from dashboard.models import TestAttempt
import random

def index(request):
    recent_attempts = TestAttempt.objects.all().order_by('-date')[:10]
    return render(request, 'mocktest/index.html', {
        'recent_attempts': recent_attempts,
    })

@login_required
def summary_view(request):
    exam_type = request.GET.get('exam_type', 'full')
    topics_breakdown = []
    total_q = 0
    
    # Get configured questions per test from settings
    questions_per_test = getattr(settings, 'QUESTIONS_PER_TEST', None)
    
    if exam_type == 'full':
        topics = ['Automation', 'Collaboration', 'DB & Security', 'Instance', 'Integration', 'Platform']
        all_qs = Question.objects.all()
        total_available = all_qs.count()
        
        if questions_per_test:
            total_q = min(total_available, questions_per_test)
        else:
            total_q = total_available
            
        for topic in topics:
            topic_count = Question.objects.filter(topic=topic).count()
            if topic_count > 0:
                topics_breakdown.append({'topic': topic, 'count': topic_count})
    elif exam_type == 'random':
        total_available = Question.objects.count()
        total_q = min(total_available, 20)
        topics_breakdown.append({'topic': 'Random Mix', 'count': total_q})
    else:
        # Topic specific
        total_available = Question.objects.filter(topic=exam_type).count()
        total_q = min(total_available, 20)
        topics_breakdown.append({'topic': exam_type, 'count': total_q})

    if total_q == 0:
        from django.contrib import messages
        messages.error(request, "No questions available for this selection.")
        return redirect('mocktest:index')
        
    return render(request, 'mocktest/summary.html', {
        'exam_type': exam_type,
        'topics_breakdown': topics_breakdown,
        'total_q': total_q,
        'total_time': total_q,
    })

@login_required
def start_test(request):
    exam_type = request.GET.get('exam_type', 'full')
    questions = []
    
    # Get configured questions per test from settings
    questions_per_test = getattr(settings, 'QUESTIONS_PER_TEST', None)
    
    if exam_type == 'full':
        all_qs = list(Question.objects.all())
        if questions_per_test:
            questions = random.sample(all_qs, min(len(all_qs), questions_per_test))
        else:
            questions = all_qs
        random.shuffle(questions)
    elif exam_type == 'random':
        all_qs = list(Question.objects.all())
        questions = random.sample(all_qs, min(len(all_qs), 20))
        random.shuffle(questions)
    else:
        # Topic specific
        topic_qs = list(Question.objects.filter(topic=exam_type))
        questions = random.sample(topic_qs, min(len(topic_qs), 20))
        random.shuffle(questions)

    # Lightweight list of question IDs to optimize load times for 400+ questions
    question_ids = [q.id for q in questions]

    return render(request, 'mocktest/mocktest.html', {
        'question_ids': question_ids,
        'timer_minutes': len(questions),
        'exam_type': exam_type,
        'total_questions': len(questions),
    })

@login_required
def get_question_api(request):
    q_id = request.GET.get('id')
    if not q_id:
        return JsonResponse({'error': 'No question ID provided'}, status=400)
    
    try:
        q = Question.objects.get(id=q_id)
        image_url = q.question_image.url if q.question_image else ''
        return JsonResponse({
            'id': q.id,
            'topic': q.topic,
            'question_type': q.question_type,
            'question_text': q.question_text,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'option_e': q.option_e or '',
            'image_url': image_url,
        })
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)

def submit_test(request):
    if request.method == 'POST':
        score   = 0
        total   = 0
        results = []

        question_ids = request.POST.getlist('question_ids')
        exam_type = request.POST.get('exam_type', 'CSA Mock Exam')
        time_taken = request.POST.get('time_taken', 'N/A')
        
        test_name_mapping = {
            'full': 'Full Syllabus Mock Test',
            'random': 'Random Mix',
        }
        test_name = test_name_mapping.get(exam_type, f'Topic: {exam_type}')

        for q_id in question_ids:
            total += 1
            question = get_object_or_404(Question, id=q_id)
            
            if question.question_type == 'SINGLE_CHOICE':
                selected = request.POST.get(f'q_{q_id}', '')
            else:
                # MULTIPLE_SELECT
                selected_list = request.POST.getlist(f'q_{q_id}')
                # Normalize and sort (e.g. ['A', 'C', 'D'])
                selected_list = sorted([s.strip() for s in selected_list if s.strip()])
                selected = ','.join(selected_list)
            
            # Normalize correct answers
            correct_list = sorted([ans.strip() for ans in question.correct_answers.split(',') if ans.strip()])
            correct_normalized = ','.join(correct_list)
            
            is_correct = (selected == correct_normalized)
            if is_correct:
                score += 1

            results.append({
                'question':   question,
                'selected':   selected,
                'is_correct': is_correct,
                'correct':    correct_normalized,
            })

        percentage = (score / total * 100) if total > 0 else 0

        if request.user.is_authenticated:
            TestAttempt.objects.create(
                user=request.user,
                score=score,
                total_questions=total,
                percentage=percentage,
                test_name=test_name
            )

        return render(request, 'mocktest/results.html', {
            'score':      score,
            'total':      total,
            'percentage': percentage,
            'results':    results,
            'passed':     percentage >= 70,
            'test_name':  test_name,
            'time_taken': time_taken,
        })

    return redirect('mocktest:index')

