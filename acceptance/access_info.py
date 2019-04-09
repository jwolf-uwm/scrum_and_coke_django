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



    def test_valid_access_admin(self):
        self.ui.command("Login admin@uwm.edu adminPass")
        self.assertEqual(self.ui.command("AccessInfo"), "NAME           PHONE           EMAIL           PASSWORD"
                                                        "Dave Brubeck   414.123.4567    admin@uwm.edu   adminPass"
                                                        "Donna Summer   414.987.6543    super@uwm.edu   superPass"
                                                        "Dean Martin    262.123.4567    instr@uwm.edu   instrPass"
                                                        "Daniel Craig   262.987.6543    t_ayy@uwm.edu   t_ayyPass")

    def test_valid_access_super(self):
        self.ui.command("Login super@uwm.edu superPass")
        self.assertEqual(self.ui.command("AccessInfo"), "NAME           PHONE           EMAIL           PASSWORD"
                                                        "Dave Brubeck   414.123.4567    admin@uwm.edu   adminPass"
                                                        "Donna Summer   414.987.6543    super@uwm.edu   superPass"
                                                        "Dean Martin    262.123.4567    instr@uwm.edu   instrPass"
                                                        "Daniel Craig   262.987.6543    t_ayy@uwm.edu   t_ayyPass")

    def test_invalid_access_instr(self):
        self.ui.command("Login instr@uwm.edu instrPass")
        self.assertEqual(self.ui.command("AccessInfo"), "Access Denied")

    def test_invalid_access_ta(self):
        self.ui.command("Login t_ayy@uwm.edu t_ayyPass")
        self.assertEqual(self.ui.command("AccessInfo"), "Access Denied")
