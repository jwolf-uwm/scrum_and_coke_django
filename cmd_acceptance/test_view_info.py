from django.test import TestCase
from classes.CmdHandler import CmdHandler


class ViewInfoTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    def test_view_info_no_setup(self):
        self.assertEqual(self.ui.parse_command("view_info"),
                         "Please run setup before attempting to execute commands.")

    def test_command_view_info_no_login(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("view_info"),
                         "Please login first.")

    def test_command_view_info_admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_info"), ["ta_assign_admin@uwm.edu", "password", "DEFAULT",
                                                              "000.000.0000"])

    def test_command_view_info_super(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_info"), ["ta_assign_super@uwm.edu", "password", "DEFAULT",
                                                              "000.000.0000"])

    def test_command_view_info_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_info"), ["instructor@uwm.edu", "password", "DEFAULT",
                                                              "000.000.0000"])

    def test_command_view_info_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_info"), ["ta@uwm.edu", "password", "DEFAULT",
                                                              "000.000.0000"])