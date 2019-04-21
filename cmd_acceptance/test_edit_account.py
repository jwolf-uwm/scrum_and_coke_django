from django.test import TestCase
from classes.CmdHandler import CmdHandler


class EditAccountTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

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
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_admin@uwm.edu password new_password"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_admin@uwm.edu name Dr. John Tang Boyland"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_admin@uwm.edu phone_number 999.999.9999"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_admin@uwm.edu email new_email@uwm.edu"),
                         "Command successful.")

    def test_edit_sup(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_super@uwm.edu password new_password"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_super@uwm.edu name Dr. John Tang Boyland"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_super@uwm.edu phone_number 999.999.9999"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_super@uwm.edu email new_email@uwm.edu"),
                         "Command successful.")

    def test_edit_TA_as_admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu password new_password"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu name Dr. John Tang Boyland"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu phone_number 999.999.9999"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu email new_email@uwm.edu"),
                         "Command successful.")

    def test_edit_TA_as_super(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu password new_password"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu name Dr. John Tang Boyland"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu phone_number 999.999.9999"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ta@uwm.edu email new_email@uwm.edu"),
                         "Command successful.")

    def test_edit_ins_as_admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ins@uwm.edu password instructor")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu password new_password"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu name Dr. John Tang Boyland"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu phone_number 999.999.9999"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu email new_email@uwm.edu"),
                         "Command successful.")

    def test_edit_ins_as_super(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ins@uwm.edu password instructor")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu password new_password"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu name Dr. John Tang Boyland"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu phone_number 999.999.9999"),
                         "Command successful.")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu email new_email@uwm.edu"),
                         "Command successful.")

    def test_edit_as_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu email new_email@uwm.edu"),
                         "Invalid command")

    def test_edit_as_ins(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("edit_account ins@uwm.edu email new_email@uwm.edu"),
                         "Invalid command")

    def test_edit_noargs(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("edit_account"),
                         "Invalid command")

    def test_edit_invalid_args(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("edit_account ta_assign_admin@uwm.edu jajajaj new_password"),
                         "Command error.")
