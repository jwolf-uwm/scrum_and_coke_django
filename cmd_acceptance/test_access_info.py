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

    def test_command_access_info_instructor_no_class(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        big_string = self.ui.parse_command("access_info")
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[6], "Instructors:")
        self.assertEqual(parse_string[7], "DEFAULT | instructor@uwm.edu | 000.000.0000")

    def test_command_access_info_ta_no_class(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        big_string = self.ui.parse_command("access_info")
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[8], "TAs:")
        self.assertEqual(parse_string[9], "DEFAULT | ta@uwm.edu | 000.000.0000")

    def test_command_access_info_inst_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_instructor instructor@uwm.edu CS101-401")
        big_string = self.ui.parse_command("access_info")
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[8], "\tCourse: CS101-401")

    def test_command_access_info_ta_one_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        self.ui.parse_command("assign_ta ta@uwm.edu CS101-401")
        big_string = self.ui.parse_command("access_info")
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[10], "\tCourse: CS101-401")

    def test_command_access_info_just_course(self):
        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("create_course CS101-401 0")
        big_string = self.ui.parse_command("access_info")
        parse_string = big_string.split("\n")
        self.assertEqual(parse_string[12], "Courses:")
        self.assertEqual(parse_string[13], "CS101-401")

    def test_command_access_info_all_the_things(self):
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
        big_string = self.ui.parse_command("access_info")
        parse_info = big_string.split("\n")
        self.assertEqual(parse_info[0], "Administrator:")
        self.assertEqual(parse_info[1], "DEFAULT | ta_assign_admin@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[2], "")
        self.assertEqual(parse_info[3], "Supervisor:")
        self.assertEqual(parse_info[4], "DEFAULT | ta_assign_super@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[5], "")
        self.assertEqual(parse_info[6], "Instructors:")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[8], "\tCourse: CS101-401")
        self.assertEqual(parse_info[9], "")
        self.assertEqual(parse_info[10], "DEFAULT | inst2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[11], "\tCourse: CS102-401")
        self.assertEqual(parse_info[12], "")
        self.assertEqual(parse_info[13], "")
        self.assertEqual(parse_info[14], "TAs:")
        self.assertEqual(parse_info[15], "DEFAULT | ta1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[16], "\tCourse: CS101-401")
        self.assertEqual(parse_info[17], "")
        self.assertEqual(parse_info[18], "DEFAULT | ta2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[19], "\tCourse: CS102-401")
        self.assertEqual(parse_info[20], "")
        self.assertEqual(parse_info[21], "")
        self.assertEqual(parse_info[22], "Courses:")
        self.assertEqual(parse_info[23], "CS101-401")
        self.assertEqual(parse_info[24], "CS102-401")
