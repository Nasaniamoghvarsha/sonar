from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from conduit.apps.articles.models import Article, Tag
from conduit.apps.authentication.models import User
from conduit.apps.profiles.models import Profile

class ArticleSafetyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', email='test@test.com', password='password')
        self.client.force_authenticate(user=self.user)

    def test_create_article(self):
        """Ensure core article creation logic isn't broken by AI."""
        response = self.client.post('/api/articles', {
            "article": {"title": "Test", "description": "Desc", "body": "Body", "tagList": ["tag1"]}
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Article.objects.filter(title="Test").exists())