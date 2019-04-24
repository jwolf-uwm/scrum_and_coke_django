from django.test import TestCase
from classes.CmdHandler import CmdHandler


class ViewTAAssignmentsTest(TestCase):
    def setUp(self):
        self.ui = CmdHandler()

    def test_access_info_no_setup(self):
        self.assertEqual(self.ui.parse_command("access_info"),
                         "Please run setup before attempting to execute commands.")

    def test_command_view_ta_assign_no_login(self):
        self.ui.parse_command("setup")
        self.assertEqual(self.ui.parse_command("create_account ta@uwm.edu password ta"),
                         "Please login first.")

    def test_command_view_ta_assign_admin(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), "You don't have access to that command.")

    def test_command_view_ta_assign_super(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), "You don't have access to that command.")

    def test_command_view_ta_assign_instructor_no_ta(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), '')

    def test_command_view_ta_assign_ta_no_class(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), 'TA: DEFAULT | ta@uwm.edu | 000.000.0000\n\n')

    def test_command_view_ta_assign_inst_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_instructor instructor@uwm.edu CS101-401")
        self.ui.parse_command("assign_ta ta@uwm.edu CS101-401")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), 'TA: DEFAULT | ta@uwm.edu | 000.000.0000\n'
                                                                  '\tCourse: CS101-401\n\n')

    def test_command_view_ta_assign_ta_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_instructor instructor@uwm.edu CS101-401")
        self.ui.parse_command("assign_ta ta@uwm.edu CS101-401")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), 'TA: DEFAULT | ta@uwm.edu | 000.000.0000\n'
                                                                  '\tCourse: CS101-401\n\n')

    def test_command_view_ta_assign_all_the_things(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account inst1@uwm.edu password instructor")
        self.ui.parse_command("create_account inst2@uwm.edu password instructor")
        self.ui.parse_command("create_account ta1@uwm.edu password ta")
        self.ui.parse_command("create_account ta2@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("create_course CS102-401 0")
        self.ui.parse_command("assign_instructor inst1@uwm.edu CS101-401")
        self.ui.parse_command("assign_instructor inst2@uwm.edu CS102-401")
        self.ui.parse_command("assign_ta ta1@uwm.edu CS101-401")
        self.ui.parse_command("assign_ta ta2@uwm.edu CS102-401")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), "You don't have access to that command.")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta1@uwm.edu password")
        self.assertEqual(self.ui.parse_command("view_ta_assign"), 'TA: DEFAULT | ta1@uwm.edu | 000.000.0000\n'
                                                                  '\tCourse: CS101-401\n\n'
                                                                  'TA: DEFAULT | ta2@uwm.edu | 000.000.0000\n'
                                                                  '\tCourse: CS102-401\n\n')
