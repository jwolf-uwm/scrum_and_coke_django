from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class CreateCourseTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    def test_no_login_get(self):
        client = Client()
        response = client.get('/create_course/')
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
        response = client.get('/create_course/')
        # status code 200, we loaded the correct page
        self.assertEqual(response.status_code, 200)
        # since we returned a render, it has all the content of the page
        # we'll just look for the header
        self.assertContains(response, "Create Course")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # no error messages
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):

        client = Client()
        session = client.session
        session['email'] = 'super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/create_course/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/create_course/')
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
        response = client.get('/create_course/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_create_course_admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/create_course/', data={'course_id': "361", 'course_section': "401", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course has been created successfully.")

    def test_create_course_supervisor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/create_course/', data={'course_id': "361", 'course_section': "401", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course has been created successfully.")

    def test_create_course_already_exists(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "361", 'course_section': "401", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "Course has been created successfully.")

        response = client.post('/create_course/', data={'course_id': "361", 'course_section': "401", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_course_id_letters(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "ABC", 'course_section': "401", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_course_id_too_big(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "1234", 'course_section': "401", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_course_id_too_small(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "12", 'course_section': "401", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_course_section_letters(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "123", 'course_section': "ABC", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_course_section_too_big(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "123", 'course_section': "1234", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_course_section_too_small(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "123", 'course_section': "99", 'num_labs': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_num_labs_letters(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "123", 'course_section': "401", 'num_labs': "A"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_num_labs_too_big(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "123", 'course_section': "401", 'num_labs': "6"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")

    def test_create_course_num_labs_too_small(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()

        response = client.post('/create_course/', data={'course_id': "123", 'course_section': "401", 'num_labs': "-1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Course")
        self.assertContains(response, "An error occurred")
