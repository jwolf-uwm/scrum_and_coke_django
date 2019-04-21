from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class CreateAccessInfo(TestCase):

    def setUp(self):
        self.ui = CmdHandler()

    def test_no_login_get(self):

        client = Client()
        response = client.get('/access_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_instructor_get(self):

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/access_info/')
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
        response = client.get('/access_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_access_info_admin(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[0], "Administrator:")
        self.assertEqual(parse_string[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_string[2], "")
        self.assertEqual(parse_string[3], "Supervisor:")
        self.assertEqual(parse_string[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")

    def test_access_info_super(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/access_info/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        big_string = str(all_messages[0])
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[0], "Administrator:")
        self.assertEqual(parse_string[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_string[2], "")
        self.assertEqual(parse_string[3], "Supervisor:")
        self.assertEqual(parse_string[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")