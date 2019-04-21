# made by Evan

import unittest
from classes import Person
from classes import Administrator
from classes import Instructor
from classes import TA
from classes import Supervisor


class DeleteTests(unittest.TestCase):
    def setup(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")

    """
        When the delete command is entered, it takes one argument:
        - Username
        If the user has permission to delete and
        the username matches the database entry
        the user delete is successful:
        - "User deleted successfully"
        If the user does not have permission, failure:
        - "You do not have permission to delete users"
        If the username does not match or is omitted, failure:
        - "Error deleting account"
    """

    def test_delete_fromAdmin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("delete TA"), "User deleted successfully")

    def test_delete_fromSupervisor(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("delete TA"), "User deleted successfully")

    def test_delete_fromInstructor(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("delete TA"), "You do not have permission to delete users")

    def test_delete_fromTA(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("delete TA"), "You do not have permission to delete users")

    def test_delete_no_args(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("delete"), "Error deleting account")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("delete"), "Error deleting account")
        self.ui.command("logout")
        self.assertEqual(self.ui.command("delete"), "Error deleting account")

    def test_delete_wrongUsername(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("delete TA1@uwm.edu"), "Error deleting account")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("delete TA1@uwm.edu"), "Error deleting account")
        self.ui.command("logout")
