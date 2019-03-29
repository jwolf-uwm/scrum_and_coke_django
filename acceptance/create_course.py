from unittest import TestCase
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Instructor import Instructor
from classes.TA import TA


class CreateCourseTests(TestCase):
    def setup(self):
        self.Sup = Supervisor("supervisor@uwm.edu", "SupervisorPassword")
        self.Admin = Administrator("admin@uwm.edu", "AdministratorPassword")
        self.Inst = Instructor("instructor@uwm.edu", "InstructorPassword")
        self.TA = TA("ta@uwm.edu", "TAPassword")

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
    def test_command_create_course_admin(self):
        self.ui.command("login admin@uwm.edu AdministratorPassword")
        self.assertEqual(self.ui.command("create_course CS101 2"), "Created course CS101 with 2 labs.")

    def test_command_create_course_supervisor(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("create_course CS102 3"), "Created course CS102 with 3 labs.")

    def test_command_create_course_instructor(self):
        self.ui.command("login instructor@uwm.edu InstructorPassword")
        self.assertEqual(self.ui.command("create_course CS103 1"), "You are not authorized to create courses.")

    def test_command_create_course_ta(self):
        self.ui.command("login ta@uwm.edu TAPassword")
        self.assertEqual(self.ui.command("create_course CS103 1"), "You are not authorized to create courses.")

    def test_command_create_course_no_title(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("create_course 1"), "Error creating course.")

    def test_command_create_course_no_num_labs(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("create_course CS103"), "Error creating course.")

    def test_command_create_course_already_exists(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("create_course CS101 2"), "Course already exists.")
