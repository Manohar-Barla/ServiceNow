import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicenow_csa.settings')
django.setup()

from syllabus.models import Domain
from practice.models import Question

def seed_questions():
    # Get domains
    platform = Domain.objects.get(name="Platform")
    db_security = Domain.objects.get(name="DB & Security")
    
    questions_data = [
        {
            "domain": platform,
            "question_text": "Which of the following is used to change the look and feel of the ServiceNow instance?",
            "option1": "UI Policy",
            "option2": "Branding Editor",
            "option3": "Business Rule",
            "option4": "Data Policy",
            "correct_answer": "2",
            "explanation": "The Branding Editor allows you to change the logo, colors, and title of your instance."
        },
        {
            "domain": db_security,
            "question_text": "What does ACL stand for in ServiceNow?",
            "option1": "Access Control List",
            "option2": "Automated Control Layer",
            "option3": "Application Control Level",
            "option4": "Advanced Configuration Log",
            "correct_answer": "1",
            "explanation": "ACL stands for Access Control List, which is used to restrict access to data."
        },
        {
            "domain": platform,
            "question_text": "Where do you go to view a list of all tables in the database?",
            "option1": "Tables & Columns",
            "option2": "Dictionary",
            "option3": "Schema Map",
            "option4": "All of the above",
            "correct_answer": "4",
            "explanation": "Tables & Columns, Dictionary, and Schema Map all provide information about tables."
        }
    ]

    for q in questions_data:
        question, created = Question.objects.get_or_create(
            question_text=q['question_text'],
            defaults={
                'domain': q['domain'],
                'option1': q['option1'],
                'option2': q['option2'],
                'option3': q['option3'],
                'option4': q['option4'],
                'correct_answer': q['correct_answer'],
                'explanation': q['explanation']
            }
        )
        if created:
            print(f"Created Question: {question.question_text[:30]}")
        else:
            print(f"Question already exists: {question.question_text[:30]}")

if __name__ == "__main__":
    seed_questions()
    print("Questions seeding completed.")
