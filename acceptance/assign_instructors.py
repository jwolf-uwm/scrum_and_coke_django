from django.test import TestCase
from classes.CmdHandler import CmdHandler


class AssignInstructorTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    """
        Assigning an instructor requires user logged in as Supervisor or Administrator.
        When the create account command is entered, it takes two arguments:
            - Instructor ID
            - Course ID
        If the course does not currently have an instructor, assigns instructor to that course and
        is successful:
        - "Instructor *Instructor Name* assigned to class *Class Name*."
        If the course is already assigned to an instructor then failure:
        - "*Class Name* already has an instructor."
        If the Instructor ID or Course ID is omitted, failure:
        - "Invalid arguments in command."
        If attempting to assign a role that is not instructor, failure:
        - "Only instructors can be assigned to classes."
        If the user is not logged in as a Supervisor or Administrator, failure:
        - "You are not authorized to assign instructors."
        If an invalid email address is used for the instructor, failure:
        - "Invalid email address."
        If the course entered does not exist, failure:
        - "Course does not exist."
        If the instructor entered does not exist, failure:
        - "Instructor does not exist."
    """
    def test_assign_instructor_no_setup(self):
        self.assertEqual(self.ui.parse_command("assign_instructor ins1@uwm.edu CS201-401"),
                         "Please run setup before attempting to execute commands.")

    def test_create_account_no_login(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("assign_instructor ins1@uwm.edu CS201-401"),
                         "Please login first.")

    def test_assign_instructor_supervisor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account inst@uwm.edu password instructor")
        self.ui.parse_command("create_course CS201-401 3")
        self.assertEqual(self.ui.parse_command("assign_instructor inst@uwm.edu CS201-401"),
                         "command successful")

    def test_assign_instructor_administrator(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account admin@uwm.edu password administrator")
        self.ui.parse_command("logout")
        self.ui.parse_command("login admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor instructor@uwm.edu CS201-401"),
                         "Access Denied")

    def test_assign_instructor_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("login instructor@uwm.edu InstructorPassword")
        self.assertEqual(self.ui.parse_command("assign_instructor instructor@uwm.edu CS201-401"),
                         "Access Denied")

    def test_assign_instructor_TA(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("login ta@uwm.edu TAPassword")
        self.assertEqual(self.ui.parse_command("assign_instructor instructor@uwm.edu CS201-401"),
                         "Access Denied")

    def test_assign_instructor_invalid_arguments(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor instructor@uwm.edu"),
                         "Incorrect Command")

    def test_assign_instructor_assign_TA(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.assertEqual(self.ui.parse_command("assign_instructor ta@uwm.edu CS201-401"),
                         "no such instructor")

    def test_invalid_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor ins1, SomeCSClass3"), "no such instructor")

    def test_nonexistent_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_instructor ins1@uwm.edu CS400-601"), "no such course")
