import unittest
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA


class EditAccountTests(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")

        """
        Admins and supervisors have permission to edit accounts
        edit_account takes 3 arguments
            -username
            -type of info to update
            -new info
        if account edit is successful
            -"account edited" displayed
        if permission not granted
            -"do not have permission to edit accounts" displayed
        if # arguments invalid
            -"invalid number of arguments" displayed
        if data type invalid
            -"invalid data to edit"
        """

    def test_edit_admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual("edit_account ADMN@uwm.edu password admn", "account edited")
        self.assertEqual(self.ADMIN.password, "admn")
        self.assertEqual("edit_account ADMN@uwm.edu username ADMN2@uwm.edu", "account edited")
        self.assertEqual(self.ADMIN.username, "ADMN2@uwm.edu")

    def test_edit_sup(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual("edit_account SUP@uwm.edu password admn", "account edited")
        self.assertEqual(self.SUP.password, "admn")
        self.assertEqual("edit_account SUP@uwm.edu username SUP2@uwm.edu", "account edited")
        self.assertEqual(self.SUP.username, "SUP2@uwm.edu")

    def test_edit_TA(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual("edit_account TA@uwm.edu password admn", "do not have permission to edit accounts")
        self.assertEqual("edit_account TA@uwm.edu username TA3@uwm.edu", "do not have permission to edit accounts")

    def test_edit_ins(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual("edit_account INS@uwm.edu password admn", "do not have permission to edit accounts")
        self.assertEqual("edit_account INS@uwm.edu username INS3@uwm.edu", "do not have permission to edit accounts")

    def test_edit_noargs(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual("edit_account  password admn", "invalid number of arguments")
        self.assertEqual("edit_account admn", "invalid number of arguments")
        self.assertEqual("edit_account", "invalid number of arguments")

    def test_edit_invalidargs(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual("edit_account ADMN@uwm.edu jajajaj admn", "invalid data to edit")
        self.assertEqual("edit_account ADMN@uwm.edu cs250 admn", "invalid data to edit")