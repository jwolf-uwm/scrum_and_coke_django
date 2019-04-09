import unittest
from classes.TA import TA
from classes.Instructor import Instructor
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Course import Course


class AssignTACourse(unittest.TestCase):
    def setUp(self):
        self.TA1 = TA("ta1@uwm.edu", "ta1Pass")
        self.TA2 = TA("ta2@uwm.edu", "ta2Pass")
        self.TA3 = TA("ta3@uwm.edu", "ta3Pass")
        self.INS = Instructor("ins@uwm.edu", "insPass")
        self.SUP = Supervisor("sup@uwm.edu", "supPass")
        self.ADMIN = Administrator("admin@uwm.edu", "adminPass")
        self.COURSE1 = Course("CS101", 2)
        self.COURSE2 = Course("CS222", 2)

    def test_command_create_account_no_setup(self):
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Please run setup before attempting to execute commands.")

    def assign_ta_course_sup(self):
        self.ui.command("Login sup@uwm.edu supPass")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "TA1@uwm.edu was assigned to CS101")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS101"),
                         "TA2@uwm.edu was assigned to CS101")
        # fails when class has equal tas and lab sections
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "CS101's lab sections are full")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS222"),
                         "TA1@uwm.edu was assigned to CS222")

    def assign_ta_course_ins(self):
        self.ui.command("Login ins@uwm.edu insPass")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "TA1@uwm.edu was assigned to CS101")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS101"),
                         "TA2@uwm.edu was assigned to CS101")
        # fails when class has equal tas and lab sections
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "CS101's lab sections are full")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS222"),
                         "TA1@uwm.edu was assigned to CS222")

    def assign_ta_course_args_dne(self):
        self.assertEqual(self.ui.command("assign_ta_course ta1 CS101"),
                         "Invalid email address")
        self.assertEqual(self.ui.command("assign_ta_course ta4@uwm.edu, CS101"),
                         "TA4@uwm.edu could not be assigned since it does not exist")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu, CS999"),
                         "CS999 could not be assigned since it does not exist")

    def assign_ta_course_num_args(self):
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu"), "Error: too few arguments")
        self.assertEqual(self.ui.command("assign_ta_course"), "Error: too few arguments")

    def assign_ta_course_non_ta(self):
        self.assertEqual(self.ui.command("assign_ta_course INS@uwm.edu CS101"),
                         "Error: INS@uwm.edu is not a TA")
        self.assertEqual(self.ui.command("assign_ta_course SUP@uwm.edu CS101"),
                         "Error: SUP@uwm.edu is not a TA")
        self.assertEqual(self.ui.command("assign_ta_course ADMIN@uwm.edu CS101"),
                         "Error: ADMIN@uwm.edu is not a TA")

    def assign_ta_course_wrong_account(self):
        self.ui.command("Login admin@uwm.edu adminPass")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS222"),
                         "Error: You don not have access to this command")
        self.ui.command("Logout")
        self.ui.command("Login ta1@uwm.edu ta1Pass")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS222"),
                         "Error: You don not have access to this command")
