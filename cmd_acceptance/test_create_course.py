from django.test import TestCase
from classes.CmdHandler import CmdHandler


class CreateCourseTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()


    """
    When the create course cmd is entered, it takes < 3 > arguments:
    - Course ID
    - Number of Labs
    If Title and lab fields are filled in, create course is a success:
    - "Created course *Course* with *x* labs."
    If user is not an Administrator or Instructor, failure:
    - "You are not authorized to create courses."
    If Title field is omitted, failure:
    - "Error creating course."
    If Instructor field is omitted, failure:
    - "Error creating course."
    If Title already exists, failure:
    - "Course already exists."
    """
    def test_create_course_admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_course CS361-401 3"), "CS361-401 has been created successfully.")

    def test_create_course_supervisor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_course CS361-401 3"), "CS361-401 has been created successfully.")

    def test_create_course_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_course CS361-401 3"),
                         "Yeah, you don't have access to that command. Nice try buddy.")

    def test_create_course_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_course CS361-401 3"),
                         "Yeah, you don't have access to that command. Nice try buddy.")

    def test_create_course_no_title(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_course 3"),
                         "Command not of the right format: [create_course CS###-### #]")

    def test_command_create_course_no_num_labs(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_course CS361-401"),
                         "Command not of the right format: [create_course CS###-### #]")

    def test_command_create_course_already_exists(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_course CS361-401 3")
        self.assertEqual(self.ui.parse_command("create_course CS361-401 3"), "An error occurred")
