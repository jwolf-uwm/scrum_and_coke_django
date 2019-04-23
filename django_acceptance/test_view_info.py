from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class ViewInfoTests(TestCase):

    def setUp(self):
        self.ui = CmdHandler()

    def test_no_login_get(self):

        client = Client()
        response = client.get('/edit_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):

        self.ui.parse_command("setup")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta_assign_admin@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):

        self.ui.parse_command("setup")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta_assign_super@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "instructor@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_ta_get(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Current Email:")
        self.assertContains(response, "ta@uwm.edu")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)