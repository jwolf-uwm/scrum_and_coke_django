from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages


class CreateAccountTests(TestCase):
    def setUp(self):
        return

    def test_no_login(self):
        client = Client()
        response = client.get('/create_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')
