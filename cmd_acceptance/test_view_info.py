from django.test import TestCase
from classes.CmdHandler import CmdHandler


class ViewInfoTests(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    def test_access_info_no_setup(self):
        self.assertEqual(self.ui.parse_command("access_info"),
                         "Please run setup before attempting to execute commands.")

