import unittest


class CreateAccountTests(unittest.TestCase):
    def setup(self):
        self.ui.command("create_user Supervisor SupervisorPassword")
        self.ui.command("create_user Administrator AdministratorPassword")
        self.ui.command("create_user Instructor InstructorPassword")
        self.ui.command("create_user TA TAPassword")

    """
        Account creation requires user logged in as Supervisor or Administrator.
        When the create account command is entered, it takes three arguments:
            - Username
            - Password
            - email address
        If the username and password do not already exist in the database, account creation
        is successful:
        - "Account created successfully."
        If the username is already taken, failure:
        - "Username already taken."
        If the username or password is omitted, failure:
        - "Invalid arguments in command."
        If the user is not logged in as a Supervisor or Administrator, failure:
        - "You are not authorized to create accounts."
    """

    def test_command_create_account_supervisor(self):
        self.ui.command("login Supervisor SupervisorPassword")
        self.assertEqual(self.ui.command("create_account newTA newTAPassword wherever@whatever.com"),
                         "Account created successfully.")

    def test_command_create_account_administrator(self):
        self.ui.command("login Administrator AdministratorPassword")
        self.assertEqual(self.ui.command("create_account newTA2 newTAPassword2 wherever2@whatever.com"),
                         "Account created successfully.")

    def test_command_create_account_instructor(self):
        self.ui.command("login Instructor InstructorPassword")
        self.assertEqual(self.ui.command("create_account newTA3 newTAPassword3 wherever3@whatever.com"),
                         "You are not authorized to create accounts.")

    def test_command_create_account_TA(self):
        self.ui.command("login TA TAPassword")
        self.assertEqual(self.ui.command("create_account newTA4 newTAPassword4 wherever4@whatever.com"),
                         "You are not authorized to create accounts.")

    def test_command_create_account_already_exists(self):
        self.ui.command("login Supervisor SupervisorPassword")
        self.assertEqual(self.ui.command("create_account newTA newTAPassword wherever@whatever.com"),
                         "Username already taken.")

    def test_command_create_account_invalid_arguments(self):
        self.ui.command("login Supervisor SupervisorPassword")
        self.assertEqual(self.ui.command("create_account newTA5 newTAPassword5"),
                         "Invalid arguments in command.")
