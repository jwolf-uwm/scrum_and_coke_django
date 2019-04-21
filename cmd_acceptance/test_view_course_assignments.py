from unittest import TestCase
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Instructor import Instructor
from classes.TA import TA
from classes.Course import Course


class ViewCourseAssignmentsTest(TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")
        self.Course1 = Course("CS351", 3)
        self.Course2 = Course("CS431", 2)
        self.Course3 = Course("CS361", 3)

    """
    an instructor has the ability to view what courses they are assigned to 
    view_course_assignments takes no arguments 
    if an instructor has no courses
        -"no courses assigned" is displayed"
    if an instructor has courses
        -each course is displayed linearly "course ta_slots"
    if an other type of user calls uses view_course_assignments
        -"access denied" is displayed 
    """

    def test_invalid_admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("view_course_assignments"), "access denied")

    def test_invalid_sup(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("view_course_assignments"), "access denied")

    def test_invalid_ta(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("view_course_assignments"), "access denied")

    def test_valid_ins(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_course_assignments"), "no courses assigned")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS361 3")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_course_assignments"), "CS361 3")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS351 3")
        self.ui.command("create_course INS@uwm.edu CS431 2")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_course_assignments"), "CS361 3 CS351 3 CS431 2")
