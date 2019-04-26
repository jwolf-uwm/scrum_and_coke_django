from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class CreateAccessInfo(TestCase):

    def setUp(self):
        self.ui = CmdHandler()

    def test_no_login_get(self):

        client = Client()
        response = client.get('/view_ta_assign/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/view_ta_assign/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_super_get(self):

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/view_ta_assign/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_view_ta_assign_instructor(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account inst@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login inst@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages)
        self.assertEqual(info_string, "[]")

    def test_view_ta_assign_ta(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\n")

    def test_view_ta_assign_instructor_no_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("setup")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages)
        self.assertEqual(info_string, "[]")

    def test_view_ta_assign_ta_no_class(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\n")

    def test_view_ta_assign_inst_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_ta ta@uwm.edu CS101-401")
        self.ui.parse_command("setup")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\tCourse: CS101-401\n\n")

    def test_view_ta_assign_ta_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_ta ta@uwm.edu CS101-401")
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\tCourse: CS101-401\n\n")

    def test_view_ta_assign_all_the_things(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account inst1@uwm.edu password instructor")
        self.ui.parse_command("create_account inst2@uwm.edu password instructor")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_account ta1@uwm.edu password ta")
        self.ui.parse_command("create_account ta2@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("create_course CS102-401 0")
        self.ui.parse_command("assign_instructor inst1@uwm.edu CS101-401")
        self.ui.parse_command("assign_instructor inst2@uwm.edu CS102-401")
        self.ui.parse_command("assign_ta ta1@uwm.edu CS101-401")
        self.ui.parse_command("assign_ta ta2@uwm.edu CS102-401")
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/view_ta_assign/')
        self.assertEqual(response.status_code, 200)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        info_string = str(all_messages[0])
        self.assertEqual(info_string, "TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\n"
                                      "TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n"
                                      "\tCourse: CS101-401\n\n"
                                      "TA: DEFAULT | ta2@uwm.edu | 000.000.0000\n"
                                      "\tCourse: CS102-401\n\n")
