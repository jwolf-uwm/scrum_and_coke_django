from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class EditInfoTests(TestCase):

    def setUp(self):
        self.ui = CmdHandler()

    def test_no_login_get(self):

        client = Client()
        response = client.get('/edit_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')