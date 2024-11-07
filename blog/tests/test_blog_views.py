from django.test import TestCase
from django.urls import reverse

class HomeTest(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse("blog:home"))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, World!", response.content)
