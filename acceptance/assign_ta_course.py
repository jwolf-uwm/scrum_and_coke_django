from django.test import TestCase
from classes.CmdHandler import CmdHandler


class AssignTACourse(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    def test_assign_ta_no_setup(self):
        self.assertEqual(self.ui.parse_command("assign_instructor ins1@uwm.edu CS201-401"),
                         "Please run setup before attempting to execute commands.")

    def test_assign_ta_no_login(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("assign_instructor ins1@uwm.edu CS201-401"),
                         "Please login first.")

    def test_assign_ta_course_sup(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS201-401 3")
        self.assertEqual(self.ui.parse_command("assign_ta ta@uwm.edu CS201-401"),
                         "command successful")

    def test_assign_ta_course_ins(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account inst@uwm.edu password instructor")
        self.ui.parse_command("create_course CS201-401 3")
        self.ui.parse_command("logout")
        self.ui.parse_command("login inst@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_ta inst@uwm.edu CS201-401"),
                         "Access Denied")

    def test_assign_instructor_administrator(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_ta ta@uwm.edu CS201-401"),
                         "Access Denied")

    def test_assign_instructor_TA(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu TAPassword ta")
        self.ui.parse_command("create_course CS201-401 3")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu TAPassword")
        self.assertEqual(self.ui.parse_command("assign_ta inst@uwm.edu CS201-401"),
                         "Access Denied")

    def test_assign_ta_course_course_dne(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.assertEqual(self.ui.parse_command("assign_ta ta@uwm.edu CS400-601"), "no such course")

    def test_assign_ta_course_ta_dne(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_course CS400-601 4")
        self.assertEqual(self.ui.parse_command("assign_ta ta@uwm.edu CS400-601"), "no such ta")

    def test_assign_ta_course_num_args(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("assign_ta instructor@uwm.edu"),
                         "Incorrect Command")

    def test_assign_ta_course_non_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ins@uwm.edu password instructor")
        self.assertEqual(self.ui.parse_command("assign_ta instructor@uwm.edu CS201-401"),
                         "no such ta")

