from django.test import TestCase
from classes.CmdHandler import CmdHandler


class CreateAccountTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    """
        Account creation requires user logged in as Supervisor or Administrator.
        When the create account command is entered, it takes three arguments:
            - Username
            - Password
            - email address
        If the username and password do not already exist in the database, account creation
        is successful.
        If the username is already taken, failure.
        If the username or password is omitted, failure.
        If the user is not logged in as a Supervisor or Administrator, failure.
    """

    def test_command_create_account_no_setup(self):
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Please run setup before attempting to execute commands.")

    def test_command_create_account_no_login(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Please login first.")

    def test_command_create_account_supervisor_make_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Account created!")

    def test_command_create_account_administrator_make_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Account created!")

    def test_command_create_account_supervisor_make_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account inst@uwm.edu password instructor"),
                         "Account created!")

    def test_command_create_account_administrator_make_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account inst@uwm.edu password instructor"),
                         "Account created!")

    def test_command_create_account_instructor(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account inst@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login inst@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Invalid command.")

    def test_command_create_account_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account inst@uwm.edu password instructor"),
                         "Invalid command.")

    def test_command_create_account_already_exists(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Account creation error.")

    def test_command_create_account_invalid_type(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password horse"),
                         "Account creation error.")

    def test_command_create_account_invalid_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.com password horse"),
                         "Account creation error.")

    def test_command_create_account_weird_email(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu.uwm.edu password ta"),
                         "Account creation error.")

    def test_command_create_account_missing_arg(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu ta"), "Invalid command.")

    def test_command_create_account_too_many_args(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta hi"), "Invalid command.")
