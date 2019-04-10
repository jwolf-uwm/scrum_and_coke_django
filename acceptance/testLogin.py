from django.test import TestCase
from classes.CmdHandler import CmdHandler


class LoginTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()
    """
    When a user wants to login two arguments are required
        -Username
        -password
    the password must match the password for the given username
    if login is successful
        -"login successful" displayed"
    if password is incorrect
        -"password invalid" displayed
    if username does not exist
        -"no such user" displayed
    """

    def test_valid_login_Admin(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("login ta_assign_admin@uwm.edu password"), "Login successful")
        self.assertEqual(self.ui.parse_command("login ta_assign_admin@uwm.edu password"), "User already logged in")
        self.ui.parse_command("logout")
        self.assertEqual(self.ui.parse_command("login ta_assign_admin@uwm.edu wrong"), "Invalid login info")

    def test_valid_login_TA(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("login ta_assign_admin@uwm.edu password"), "Login successful")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.assertEqual(self.ui.parse_command("login ta@uwm.edu password"), "Login successful")
        self.ui.parse_command("logout")
        self.assertEqual(self.ui.parse_command("login ta@uwm.edu wrong"), "Invalid login info")

    def test_valid_login_Instructor(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("login ta_assign_admin@uwm.edu password"), "Login successful")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.assertEqual(self.ui.parse_command("login instructor@uwm.edu wrong"), "Invalid login info")
        self.assertEqual(self.ui.parse_command("login instructor@uwm.edu password"), "Login successful")
        self.ui.parse_command("logout")

    def test_valid_login_Supervisor(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("login ta_assign_super@uwm.edu password"), "Login successful")
        self.assertEqual(self.ui.parse_command("login ta_assign_super@uwm.edu password"), "User already logged in")
        self.ui.parse_command("logout")
        self.assertEqual(self.ui.parse_command("login ta_assign_super@uwm.edu wrong"), "Invalid login info")
