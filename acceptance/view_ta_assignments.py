import unittest
from classes.TA import TA
from classes.Instructor import Instructor
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Course import Course


class ViewTAAssignmentsTest(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")
        self.TA = TA("TA1@uwm.edu", "TA1")
        self.TA = TA("TA2@uwm.edu", "TA2")
        self.Course1 = Course("CS351", 3)
        self.Course2 = Course("CS431", 2)
        self.Course3 = Course("CS361", 3)

    """
    A TA has the ability to view all TA course assignments
    view_ta_assignments takes no arguments
    
    if a TA calls it
        - List of each course and the TA(s) assigned to it
        
    if a Instructor calls it
        - List of each course and the TA(s) assigned to it
        
    if a admin or sup calls it
        - "access denied" is displayed
        
    if there are no courses
        -"no courses" is displayed
        
    if a course doesnt have a TA
        -"No TA" is displayed after the course
    """

    def test_invalid_admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("view_ta_assignments"), "access denied")

    def test_invalid_sup(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("view_ta_assignments"), "access denied")

    def test_valid_ta(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("view_ta_assignments"), "no courses")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS361 3")
        self.ui.command("logout")
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS351 3")
        self.ui.command("assign_ta_course TA@uwm.edu CS351 3")
        self.ui.command("create_course INS@uwm.edu CS431 2")
        self.ui.command("assign_ta_course TA@uwm.edu CS431 2")
        self.ui.command("assign_ta_course TA1@uwm.edu CS431 2")
        self.ui.command("logout")
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA, CS351 3: TA, CS431 2: TA TA1")

    def test_valid_ins(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_ta_assignments"), "no courses")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS361 3")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS351 3")
        self.ui.command("assign_ta_course TA@uwm.edu CS351 3")
        self.ui.command("assign_ta_course TA1@uwm.edu CS351 2")
        self.ui.command("assign_ta_course TA2@uwm.edu CS351 2")
        self.ui.command("create_course INS@uwm.edu CS431 2")
        self.ui.command("assign_ta_course TA@uwm.edu CS431 2")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA, CS351 3: TA TA1 TA2, CS431 2: TA")
