from django.shortcuts import render, get_object_or_404, redirect
from question_manager.models import Question

def index(request):
    topics = []
    for val, name in Question.TOPIC_CHOICES:
        count = Question.objects.filter(topic=val).count()
        topics.append({
            'id': val,
            'name': name,
            'count': count
        })
    return render(request, 'practice/practice_home.html', {'topics': topics})

def practice_by_topic(request, topic_name):
    questions = Question.objects.filter(topic=topic_name).order_by('id')
    return render(request, 'practice/practice_questions.html', {
        'topic_name': topic_name,
        'questions': questions,
    })

def quiz_view(request, topic_name):
    questions = Question.objects.filter(topic=topic_name).order_by('id')
    
    results = None
    if request.method == 'POST':
        results = []
        for q in questions:
            if q.question_type == 'SINGLE_CHOICE':
                selected = request.POST.get(f'q_{q.id}', '')
            else:
                selected_list = request.POST.getlist(f'q_{q.id}')
                selected_list = sorted([s.strip() for s in selected_list if s.strip()])
                selected = ','.join(selected_list)
                
            correct_list = sorted([ans.strip() for ans in q.correct_answers.split(',') if ans.strip()])
            correct_normalized = ','.join(correct_list)
            
            is_correct = (selected == correct_normalized)
            results.append({
                'question': q,
                'selected': selected,
                'is_correct': is_correct,
                'correct': correct_normalized
            })

    return render(request, 'practice/quiz.html', {
        'topic_name': topic_name,
        'questions': questions,
        'results': results,
    })
