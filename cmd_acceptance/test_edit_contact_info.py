from django.test import TestCase
from classes.CmdHandler import CmdHandler


class EditContactInfoTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    def test_command_create_account_no_setup(self):
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.edu"),
                         "Please run setup before attempting to execute commands.")

    def test_command_create_account_no_login(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.edu"),
                         "Please login first.")

    def test_command_admin_change_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.edu"), "Email address changed.")

    def test_command_super_change_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.edu"), "Email address changed.")

    def test_command_instructor_change_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.edu"), "Email address changed.")

    def test_command_ta_change_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.edu"), "Email address changed.")

    def test_command_bad_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.com"), "Invalid/taken email address.")

    def test_command_no_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_email"), "Parameter error.")

    def test_command_weird_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_email change_me@uwm.com@uwm.com"),
                         "Invalid/taken email address.")

    def test_command_admin_change_password(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_password 12345"), "Password changed.")

    def test_command_super_change_password(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_password 12345"), "Password changed.")

    def test_command_instructor_change_password(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_password 12345"), "Password changed.")

    def test_command_ta_change_password(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_password 12345"), "Password changed.")

    def test_command_no_password(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_password"), "Parameter error.")

    def test_command_admin_change_name(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_name changeguy"), "Name changed.")

    def test_command_super_change_name(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_name changeguy"), "Name changed.")

    def test_command_instructor_change_name(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_name changeguy"), "Name changed.")

    def test_command_ta_change_name(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_name changeguy"), "Name changed.")

    def test_command_change_multiple_name(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_name Joe Bob Henry Bob Bob"), "Name changed.")

    def test_command_change_no_name(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_name"), "Parameter error.")

    def test_command_admin_change_phone(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_phone 414.867.5309"), "Phone number changed.")

    def test_command_super_change_phone(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_phone 414.867.5309"), "Phone number changed.")

    def test_command_instructor_change_phone(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_phone 414.867.5309"), "Phone number changed.")

    def test_command_ta_change_phone(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_phone 414.867.5309"), "Phone number changed.")

    def test_command_bad_phone(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_phone 414-867-5309"), "Invalid phone format.")

    def test_command_bad_phone_two(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_phone 4148675309"), "Invalid phone format.")

    def test_command_no_phone(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("change_phone"), "Parameter error.")
