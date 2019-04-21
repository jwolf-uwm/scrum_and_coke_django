from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class CreateAccountTests(TestCase):

    def setUp(self):
        return

    def test_no_login_get(self):

        client = Client()
        response = client.get('/create_account/')
        # this gets any messages
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # this should be the first and only message, tagged error
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        # since we returned a redirect, we can check the location
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):

        client = Client()
        # make a session, email and type are all you need
        session = client.session
        session['email'] = 'admin@uwm.edu'
        session['type'] = 'administrator'
        # save the session
        session.save()
        response = client.get('/create_account/', follow="true")
        # status code 200, we loaded the correct page
        self.assertEqual(response.status_code, 200)
        # since we returned a render, it has all the content of the page
        # we'll just look for the header
        self.assertContains(response, "Create Account")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # no error messages
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):

        client = Client()
        session = client.session
        session['email'] = 'super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/create_account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Account")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/create_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_ta_get(self):

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/create_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_admin_create_ta(self):
        self.ui = CmdHandler()
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'admin@uwm.edu'
        session['type'] = 'admin'
        session.save()
        response = client.post('/create_account/', data={'email': "grant@uwm.edu", 'password': "grant",
                                                         'type': "ta"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Account")
        self.assertContains(response, "Account created!")
