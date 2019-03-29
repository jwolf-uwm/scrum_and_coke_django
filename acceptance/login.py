import unittest
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")
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
        self.assertEqual(self.ui.command("Login ADMN@uwm.edu ADMN "), "login successful")

    def test_invalid_login_Admin(self):
        self.assertEqual(self.ui.command("Login ADMN@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login ADMN3@uwm.edu AdminPassword"), "No such user")

    def test_valid_login_TA(self):
        self.assertEqual(self.ui.command("Login TA@uwm.edu TA "), "login successful")

    def test_invalid_login_TA(self):
        self.assertEqual(self.ui.command("Login TA@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login TA2@uwm.edu TAPassword"), "No such user")

    def test_valid_login_Instructor(self):
        self.assertEqual(self.ui.command("Login INS@uwm.edu INS "), "login successful")

    def test_invalid_login_Instructor(self):
        self.assertEqual(self.ui.command("Login INS@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login INS2@uwm.edu InstructorPassword"), "No such user")

    def test_valid_login_Supervisor(self):
        self.assertEqual(self.ui.command("Login SUP@uwm.edu SUP "), "login successful")

    def test_invalid_login_Admin(self):
        self.assertEqual(self.ui.command("Login SUP@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login SUP2@uwm.edu SupervisorPassword"), "No such user")

    def test_invalid_number_args(self):
        self.assertEqual(self.ui.command("Login AdminPaword "), "invalid number of arguments")
        self.assertEqual(self.ui.command("Login SUP@uwm.edu "), "invalid number of arguments")
