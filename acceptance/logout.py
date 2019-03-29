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
    When a user wants to logout no arguments are required 
    if logout works properly
        -"logout successful"
    if logout does not work
        -"logout failed"
    """

    def test_logout_Admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_logout_TA(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_logout_Instructor(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_logout_Supervisor(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_invalid_logout(self):
        self.assertEqual(self.ui.command("logout"), "logout failed")