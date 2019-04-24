from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler
from ta_assign import models


class LoginTests(TestCase):

    def setUp(self):
        self.ui = CmdHandler()

    def test_login(self):

        self.ui.parse_command("setup")
        client = Client()
        response = client.post("/login/", data={'email': "ta_assign_super@uwm.edu", 'password': "password"}, follow="true")
        session = client.session
        self.assertEqual(session["email"], "ta_assign_super@uwm.edu")
        self.assertEqual(session["type"], "supervisor")
        self.assertEqual(response.status_code, 200)

    def test_bad_login(self):

        self.ui.parse_command("setup")
        client = Client()
        response = client.post("/login/", data={'email': "ta_super@uwm.edu", 'password': "password"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username/password incorrect")

    def test_bad_password_login(self):

        self.ui.parse_command("setup")
        client = Client()
        response = client.post("/login/", data={'email': "ta_assign_super@uwm.edu", 'password': "passwor"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username/password incorrect")

    def test_already_login(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/login/')
        self.assertEqual(response.get('location'), '/index/')
