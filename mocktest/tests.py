from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from question_manager.models import Question

class MockTestViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teststudent', password='studentPassword123!')
        
        # Seed a test question
        self.question = Question.objects.create(
            question_number=1,
            question_type='SINGLE_CHOICE',
            topic='Automation',
            question_text='What is the primary function of Flow Designer?',
            option_a='To automate processes',
            option_b='To design databases',
            option_c='To style pages',
            option_d='To build charts',
            correct_answers='A'
        )

    def test_unauthenticated_redirection(self):
        """Verify summary_view and start_test redirect to login if unauthenticated."""
        summary_url = reverse('mocktest:summary')
        start_url = reverse('mocktest:start')
        
        response1 = self.client.get(summary_url)
        self.assertEqual(response1.status_code, 302)
        self.assertIn('/login', response1.url)

        response2 = self.client.get(start_url)
        self.assertEqual(response2.status_code, 302)
        self.assertIn('/login', response2.url)

    def test_summary_view(self):
        """Verify summary_view loads correctly for authenticated candidate."""
        self.client.login(username='teststudent', password='studentPassword123!')
        summary_url = reverse('mocktest:summary') + '?exam_type=full'
        
        response = self.client.get(summary_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mocktest/summary.html')
        self.assertIn('total_q', response.context)
        self.assertEqual(response.context['total_q'], 1)

    def test_start_test_view(self):
        """Verify start_test view generates and shuffles question ID lists instead of loading heavy objects."""
        self.client.login(username='teststudent', password='studentPassword123!')
        start_url = reverse('mocktest:start') + '?exam_type=full'
        
        response = self.client.get(start_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mocktest/mocktest.html')
        self.assertIn('question_ids', response.context)
        self.assertEqual(response.context['question_ids'], [self.question.id])

    def test_get_question_api_valid(self):
        """Verify dynamic AJAX API view get_question_api succeeds for a valid ID."""
        self.client.login(username='teststudent', password='studentPassword123!')
        api_url = reverse('mocktest:api_get_question') + f'?id={self.question.id}'
        
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        self.assertEqual(data['id'], self.question.id)
        self.assertEqual(data['topic'], 'Automation')
        self.assertEqual(data['question_text'], 'What is the primary function of Flow Designer?')
        self.assertEqual(data['option_a'], 'To automate processes')

    def test_get_question_api_invalid(self):
        """Verify get_question_api returns 404 for invalid question IDs."""
        self.client.login(username='teststudent', password='studentPassword123!')
        api_url = reverse('mocktest:api_get_question') + '?id=99999'
        
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 404)
