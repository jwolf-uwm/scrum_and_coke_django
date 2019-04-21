from django.test import TestCase
from classes.CmdHandler import CmdHandler


class LogoutTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()
    """
    When a user wants to logout no arguments are required 
    if logout works properly
        -"logout successful"
    if logout does not work
        -"logout failed"
    """

    def test_logout_Admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("login ADMN@uwm.edu ADMIN")
        self.assertTrue(self.ui.parse_command("logout"))

    def test_logout_TA(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("login TA@uwm.edu TA")
        self.assertTrue(self.ui.parse_command("logout"))

    def test_logout_Instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("login INS@uwm.edu INS")
        self.assertTrue(self.ui.parse_command("logout"))

    def test_logout_Supervisor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("login SUP@uwm.edu SUP")
        self.assertTrue(self.ui.parse_command("logout"))

    def test_invalid_logout(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("logout"), "Please login first.")
