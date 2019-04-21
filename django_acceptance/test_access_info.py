from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class CreateAccessInfo(TestCase):

    def setUp(self):
        return

    def test_no_login_get(self):

        client = Client()
        response = client.get('/access_info/')
        # this gets any messages
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # this should be the first and only message, tagged error
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        # since we returned a redirect, we can check the location
        self.assertEqual(response.get('location'), '/login/')
