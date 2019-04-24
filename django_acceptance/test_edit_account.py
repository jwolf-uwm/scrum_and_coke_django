from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class EditInfoTests(TestCase):

    def setUp(self):
        self.ui = CmdHandler()
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")

    def test_no_login_get(self):
        client = Client()
        response = client.get('/edit_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):
        client = Client()
        session = client.session
        session['email'] = 'admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/edit_account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):
        client = Client()
        session = client.session
        session['email'] = 'super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/edit_account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):
        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/edit_account/')
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
        response = client.get('/edit_account/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_admin_edit_admin_email(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_admin_password(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_admin_name(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_admin_phone(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_super_email(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_super_password(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_super_name(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_super_phone(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_instructor_email(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_instructor_password(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_instructor_name(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_instructor_phone(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_ta_email(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_ta_password(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_ta_name(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_admin_edit_ta_phone(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_admin_email(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_admin_password(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_admin_name(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_admin_phone(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_super_email(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_super_password(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_super_name(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_super_phone(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_super@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_instructor_email(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_instructor_password(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_instructor_name(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_instructor_phone(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "instructor@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_ta_email(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "email",
                                                       'data': "new_email@uwm.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_ta_password(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "password",
                                                       'data': "new_password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_ta_name(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "name",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_super_edit_ta_phone(self):
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta@uwm.edu", 'field': "phone",
                                                       'data': "414.123.4567"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command successful.")

    def test_edit_bad_email(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "BAD_EMAIL@uwm.com"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command error")

    def test_edit_bad_email_too_many_args(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "email",
                                                       'data': "BAD_EMAIL@uwm.edu otherstuff"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Invalid command")

    def test_edit_bad_phone_too_long(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.12345"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command error")

    def test_edit_bad_phone_too_short(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command error")

    def test_edit_bad_phone_wrong_format(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123-123-1234"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command error")

    def test_edit_bad_phone_non_digits(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.ABCD"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Command error")

    def test_edit_bad_phone_too_many_args(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "phone",
                                                       'data': "123.123.1234 otherstuff"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Invalid command")

    def test_edit_account_bad_field(self):
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/edit_account/', data={'email': "ta_assign_admin@uwm.edu", 'field': "nombre",
                                                       'data': "Dr. John Tang Boyland"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Account")
        self.assertContains(response, "Invalid command")


