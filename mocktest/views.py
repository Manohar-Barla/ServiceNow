from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    
    if exam_type == 'full':
        topics_weight = {
            'Automation': 12, 'Collaboration': 9, 'DB & Security': 12,
            'Instance': 9, 'Integration': 9, 'Platform': 9
        }
        for topic, target in topics_weight.items():
            actual = min(Question.objects.filter(topic=topic).count(), target)
            topics_breakdown.append({'topic': topic, 'count': actual})
            total_q += actual
    elif exam_type == 'random':
        actual = min(Question.objects.count(), 20)
        topics_breakdown.append({'topic': 'Random Mix', 'count': actual})
        total_q += actual
    else:
        actual = min(Question.objects.filter(topic=exam_type).count(), 20)
        topics_breakdown.append({'topic': exam_type, 'count': actual})
        total_q += actual

    if total_q == 0:
        from django.contrib import messages
        messages.error(request, "No questions available for this topic.")
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
    
    if exam_type == 'full':
        # Weightage: 60 total questions
        # Automation 20% (12), Collaboration 15% (9), DB & Security 20% (12)
        # Instance 15% (9), Integration 15% (9), Platform 15% (9)
        topics_weight = {
            'Automation': 12,
            'Collaboration': 9,
            'DB & Security': 12,
            'Instance': 9,
            'Integration': 9,
            'Platform': 9
        }
        
        for topic, count in topics_weight.items():
            topic_qs = list(Question.objects.filter(topic=topic))
            questions.extend(random.sample(topic_qs, min(len(topic_qs), count)))
            
        random.shuffle(questions)
        
    elif exam_type == 'random':
        all_qs = list(Question.objects.all())
        questions = random.sample(all_qs, min(len(all_qs), 20))
    else:
        # Topic specific
        topic_qs = list(Question.objects.filter(topic=exam_type))
        questions = random.sample(topic_qs, min(len(topic_qs), 20))

    return render(request, 'mocktest/mocktest.html', {
        'questions': questions,
        'timer_minutes': len(questions),
        'exam_type': exam_type,
    })

def submit_test(request):
    if request.method == 'POST':
        score   = 0
        total   = 0
        results = []

        question_ids = request.POST.getlist('question_ids')
        exam_type = request.POST.get('exam_type', 'CSA Mock Exam')
        
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
        })

    return redirect('mocktest:index')
