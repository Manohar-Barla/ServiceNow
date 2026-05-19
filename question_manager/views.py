from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Question
from .forms import QuestionForm, BulkUploadForm
from .utils import parse_questions_file

def is_admin_or_dummy(user):
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role in ['ADMIN', 'DUMMY']
    except Exception:
        return False

@login_required
@user_passes_test(is_admin_or_dummy, login_url='home')
def dashboard(request):
    questions = Question.objects.all().order_by('id')
    
    # Filtering
    topic_filter = request.GET.get('topic')
    type_filter = request.GET.get('type')
    search_query = request.GET.get('search')
    
    if topic_filter:
        questions = questions.filter(topic=topic_filter)
    if type_filter:
        questions = questions.filter(question_type=type_filter)
    if search_query:
        questions = questions.filter(question_text__icontains=search_query)
        
    context = {
        'questions': questions,
        'topics': Question.TOPIC_CHOICES,
        'types': Question.TYPE_CHOICES,
        'current_topic': topic_filter,
        'current_type': type_filter,
        'search_query': search_query,
    }
    return render(request, 'question_manager/dashboard.html', context)

@login_required
@user_passes_test(is_admin_or_dummy, login_url='home')
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Question added successfully.")
            return redirect('question_manager:dashboard')
    else:
        form = QuestionForm()
    return render(request, 'question_manager/form.html', {'form': form, 'title': 'Add Question'})

@login_required
@user_passes_test(is_admin_or_dummy, login_url='home')
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully.")
            return redirect('question_manager:dashboard')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question_manager/form.html', {'form': form, 'title': 'Edit Question'})

@login_required
@user_passes_test(is_admin_or_dummy, login_url='home')
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question deleted successfully.")
        return redirect('question_manager:dashboard')
    return render(request, 'question_manager/dashboard.html') # A post-only form might be better in modal, but we can do it with confirmation. Let's redirect to dashboard if GET.

@login_required
@user_passes_test(is_admin_or_dummy, login_url='home')
def preview_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question_manager/preview.html', {'question': question})

@login_required
@user_passes_test(is_admin_or_dummy, login_url='home')
def bulk_upload(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            saved_count, error_msg = parse_questions_file(uploaded_file, uploaded_file.name)
            if saved_count > 0:
                messages.success(request, f"Successfully imported {saved_count} questions.")
            if error_msg:
                messages.warning(request, f"Some errors occurred: {error_msg}")
            return redirect('question_manager:dashboard')
    else:
        form = BulkUploadForm()
    return render(request, 'question_manager/upload.html', {'form': form})
