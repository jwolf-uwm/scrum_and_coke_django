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

    def test_access_info_instructor_no_class(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
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
        self.assertEqual(parse_string[6], "Instructors:")
        self.assertEqual(parse_string[7], "DEFAULT | instructor@uwm.edu | 000.000.0000")

    def test_access_info_ta_no_class(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
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
        self.assertEqual(parse_string[8], "TAs:")
        self.assertEqual(parse_string[9], "DEFAULT | ta@uwm.edu | 000.000.0000")

    def test_access_info_inst_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_instructor instructor@uwm.edu CS101-401")
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
        self.assertEqual(parse_string[8], "Course: CS101-401")

    def test_access_info_ta_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_ta ta@uwm.edu CS101-401")
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
        self.assertEqual(parse_string[10], "Course: CS101-401")

    def test_access_info_just_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
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
        self.assertEqual(parse_string[11], "Courses:")
        self.assertEqual(parse_string[12], "CS101-401")

    def test_access_info_all_the_things(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account inst1@uwm.edu password instructor")
        self.ui.parse_command("create_account inst2@uwm.edu password instructor")
        self.ui.parse_command("create_account ta1@uwm.edu password ta")
        self.ui.parse_command("create_account ta2@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("create_course CS102-401 0")
        self.ui.parse_command("assign_instructor inst1@uwm.edu CS101-401")
        self.ui.parse_command("assign_instructor inst2@uwm.edu CS102-401")
        self.ui.parse_command("assign_ta ta1@uwm.edu CS101-401")
        self.ui.parse_command("assign_ta ta2@uwm.edu CS102-401")
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
        parse_info = big_string.split("\n")
        self.assertEqual(parse_info[0], "Administrator:")
        self.assertEqual(parse_info[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[2], "")
        self.assertEqual(parse_info[3], "Supervisor:")
        self.assertEqual(parse_info[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[5], "")
        self.assertEqual(parse_info[6], "Instructors:")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[8], "Course: CS101-401")
        self.assertEqual(parse_info[9], "DEFAULT | inst2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[10], "Course: CS102-401")
        self.assertEqual(parse_info[11], "")
        self.assertEqual(parse_info[12], "TAs:")
        self.assertEqual(parse_info[13], "DEFAULT | ta1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[14], "Course: CS101-401")
        self.assertEqual(parse_info[15], "DEFAULT | ta2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[16], "Course: CS102-401")
        self.assertEqual(parse_info[17], "")
        self.assertEqual(parse_info[18], "Courses:")
        self.assertEqual(parse_info[19], "CS101-401")
        self.assertEqual(parse_info[20], "CS102-401")