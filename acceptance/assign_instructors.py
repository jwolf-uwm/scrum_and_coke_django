from unittest import TestCase
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Instructor import Instructor
from classes.TA import TA
from classes.Course import Course


class AssignInstructorTests(TestCase):
    def setup(self):
        self.Sup = Supervisor("supervisor@uwm.edu", "SupervisorPassword")
        self.Admin = Administrator("admin@uwm.edu", "AdministratorPassword")
        self.Inst = Instructor("instructor@uwm.edu", "InstructorPassword")
        self.Inst2 = Instructor("instructor2@uwm.edu", "InstructorPassword2")
        self.TA = TA("ta@uwm.edu", "TAPassword")
        self.Course1 = Course("SomeCSClass1", 1)
        self.Course2 = Course("SomeCSClass2", 2)
        self.Course3 = Course("SomeCSClass3", 3)

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

    def test_command_assign_instructor_supervisor(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass1"),
                         "Instructor " + self.Inst.name + " assigned to " + self.Course1.course_id + ".")

    def test_command_assign_instructor_administrator(self):
        self.ui.command("login admin@uwm.edu AdministratorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass2"),
                         "Instructor " + self.Inst.name + " assigned to " + self.Course1.course_id + ".")

    def test_command_assign_instructor_instructor(self):
        self.ui.command("login instructor@uwm.edu InstructorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass3"),
                         "You are not authorized to assign instructors.")

    def test_command_assign_instructor_TA(self):
        self.ui.command("login ta@uwm.edu TAPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass3"),
                         "You are not authorized to assign instructors.")

    def test_command_assign_instructor_class_taken(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor2@uwm.edu SomeCSClass1"),
                         self.Course1.course_id + " already has an instructor.")

    def test_command_assign_instructor_invalid_arguments(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu"),
                         "Invalid arguments in command.")

    def test_command_assign_instructor_assign_TA(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ta@uwm.edu SomeCSClass3"),
                         "Only instructors can be assigned to classes.")

    def test_command_invalid_email(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ins1, SomeCSClass3"), "Invalid email address.")

    def test_command_nonexistent_course(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ins1@uwm.edu SomeCSClass4"), "Course does not exist.")

    def test_command_nonexistent_instructor(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ins4@uwm.edu SomeCSClass3"), "Instructor does not exist.")
