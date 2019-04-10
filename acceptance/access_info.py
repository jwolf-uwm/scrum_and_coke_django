from django.test import TestCase
from classes.CmdHandler import CmdHandler


class CreateAccountTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    def test_access_info_no_setup(self):
        self.assertEqual(self.ui.parse_command("access_info"),
                         "Please run setup before attempting to execute commands.")

    def test_command_access_info_no_login(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Please login first.")

    def test_command_access_info_admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        big_string = self.ui.parse_command("access_info")
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[0], "Administrator:")
        self.assertEqual(parse_string[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_string[2], "")
        self.assertEqual(parse_string[3], "Supervisor:")
        self.assertEqual(parse_string[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")

    def test_command_access_info_super(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        big_string = self.ui.parse_command("access_info")
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[0], "Administrator:")
        self.assertEqual(parse_string[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_string[2], "")
        self.assertEqual(parse_string[3], "Supervisor:")
        self.assertEqual(parse_string[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")

    def test_command_access_info_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("access_info"), "Invalid command.")

    def test_command_access_info_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("access_info"), "Invalid command.")

