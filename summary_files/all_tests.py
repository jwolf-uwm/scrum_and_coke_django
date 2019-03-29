
import unittest


class AssignInstructorTests(unittest.TestCase):
    def setup(self):
        self.Sup = Supervisor("supervisor@uwm.edu", "SupervisorPassword")
        self.Admin = Administrator("admin@uwm.edu", "AdministratorPassword")
        self.Inst = Instructor("instructor@uwm.edu", "InstructorPassword")
        self.Inst2 = Instructor("instructor2@uwm.edu", "InstructorPassword2")
        self.TA = TA("ta@uwm.edu", "TAPassword")
        self.Course1 = Course("SomeCSClass1", 1)
        self.Course2 = Course("SomeCSClass2", 2)
        self.Course3 = Course("SomeCSClass3", 3)

    """
        Assigning an instructor requires user logged in as Supervisor or Administrator.
        When the create account command is entered, it takes two arguments:
            - Instructor ID
            - Course ID
        If the course does not currently have an instructor, assigns instructor to that course and
        is successful:
        - "Instructor *Instructor Name* assigned to class *Class Name*."
        If the course is already assigned to an instructor then failure:
        - "*Class Name* already has an instructor."
        If the Instructor ID or Course ID is omitted, failure:
        - "Invalid arguments in command."
        If attempting to assign a role that is not instructor, failure:
        - "Only instructors can be assigned to classes."
        If the user is not logged in as a Supervisor or Administrator, failure:
        - "You are not authorized to assign instructors."
        If an invalid email address is used for the instructor, failure:
        - "Invalid email address."
        If the course entered does not exist, failure:
        - "Course does not exist."
        If the instructor entered does not exist, failure:
        - "Instructor does not exist."
    """

    def test_command_assign_instructor_supervisor(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass1"),
                         "Instructor " + self.Inst.name + " assigned to " + self.Course1.course_id + ".")

    def test_command_assign_instructor_administrator(self):
        self.ui.command("login admin@uwm.edu AdministratorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass2"),
                         "Instructor " + self.Inst.name + " assigned to " + self.Course1.course_id + ".")

    def test_command_assign_instructor_instructor(self):
        self.ui.command("login instructor@uwm.edu InstructorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass3"),
                         "You are not authorized to assign instructors.")

    def test_command_assign_instructor_TA(self):
        self.ui.command("login ta@uwm.edu TAPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu SomeCSClass3"),
                         "You are not authorized to assign instructors.")

    def test_command_assign_instructor_class_taken(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor2@uwm.edu SomeCSClass1"),
                         self.Course1.course_id + " already has an instructor.")

    def test_command_assign_instructor_invalid_arguments(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor instructor@uwm.edu"),
                         "Invalid arguments in command.")

    def test_command_assign_instructor_assign_TA(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ta@uwm.edu SomeCSClass3"),
                         "Only instructors can be assigned to classes.")

    def test_command_invalid_email(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ins1, SomeCSClass3"), "Invalid email address.")

    def test_command_nonexistent_course(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ins1@uwm.edu SomeCSClass4"), "Course does not exist.")

    def test_command_nonexistent_instructor(self):
        self.ui.command("login supervisor@uwm.edu SupervisorPassword")
        self.assertEqual(self.ui.command("assign_instructor ins4@uwm.edu SomeCSClass3"), "Instructor does not exist.")


import unittest
# from classes import classes.Person
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA


class AccessInfoTests(unittest.TestCase):
    def setUp(self):
        self.ADMIN = Administrator("admin@uwm.edu", "adminPass")
        self.ADMIN.change_name("Dave Brubeck")
        self.ADMIN.change_phone(4141234567)

        self.SUPER = Supervisor("super@uwm.edu", "superPass")
        self.SUPER.change_name("Donna Summer")
        self.SUPER.change_phone(4149876543)

        self.INSTR = Instructor("instr@uwm.edu", "instrPass")
        self.INSTR.change_name("Dean Martin")
        self.INSTR.change_phone(2621234567)

        self.T_AYY = TA("t_ayy@uwm.edu", "t_ayyPass")
        self.T_AYY.change_name("Daniel Craig")
        self.T_AYY.change_phone(2629876543)

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

import unittest
from classes.TA import TA
from classes.Instructor import Instructor
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Course import Course


class AssignTACourse(unittest.TestCase):
    def setUp(self):
        self.TA1 = TA("ta1@uwm.edu", "ta1Pass")
        self.TA2 = TA("ta2@uwm.edu", "ta2Pass")
        self.TA3 = TA("ta3@uwm.edu", "ta3Pass")
        self.INS = Instructor("ins@uwm.edu", "insPass")
        self.SUP = Supervisor("sup@uwm.edu", "supPass")
        self.ADMIN = Administrator("admin@uwm.edu", "adminPass")
        self.COURSE1 = Course("CS101", 2)
        self.COURSE2 = Course("CS222", 2)

    def assign_ta_course_sup(self):
        self.ui.command("Login sup@uwm.edu supPass")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "TA1@uwm.edu was assigned to CS101")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS101"),
                         "TA2@uwm.edu was assigned to CS101")
        # fails when class has equal tas and lab sections
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "CS101's lab sections are full")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS222"),
                         "TA1@uwm.edu was assigned to CS222")

    def assign_ta_course_ins(self):
        self.ui.command("Login ins@uwm.edu insPass")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "TA1@uwm.edu was assigned to CS101")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS101"),
                         "TA2@uwm.edu was assigned to CS101")
        # fails when class has equal tas and lab sections
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS101"),
                         "CS101's lab sections are full")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu CS222"),
                         "TA1@uwm.edu was assigned to CS222")

    def assign_ta_course_args_dne(self):
        self.assertEqual(self.ui.command("assign_ta_course ta1 CS101"),
                         "Invalid email address")
        self.assertEqual(self.ui.command("assign_ta_course ta4@uwm.edu, CS101"),
                         "TA4@uwm.edu could not be assigned since it does not exist")
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu, CS999"),
                         "CS999 could not be assigned since it does not exist")

    def assign_ta_course_num_args(self):
        self.assertEqual(self.ui.command("assign_ta_course ta1@uwm.edu"), "Error: too few arguments")
        self.assertEqual(self.ui.command("assign_ta_course"), "Error: too few arguments")

    def assign_ta_course_non_ta(self):
        self.assertEqual(self.ui.command("assign_ta_course INS@uwm.edu CS101"),
                         "Error: INS@uwm.edu is not a TA")
        self.assertEqual(self.ui.command("assign_ta_course SUP@uwm.edu CS101"),
                         "Error: SUP@uwm.edu is not a TA")
        self.assertEqual(self.ui.command("assign_ta_course ADMIN@uwm.edu CS101"),
                         "Error: ADMIN@uwm.edu is not a TA")

    def assign_ta_course_wrong_account(self):
        self.ui.command("Login admin@uwm.edu adminPass")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS222"),
                         "Error: You don not have access to this command")
        self.ui.command("Logout")
        self.ui.command("Login ta1@uwm.edu ta1Pass")
        self.assertEqual(self.ui.command("assign_ta_course ta2@uwm.edu CS222"),
                         "Error: You don not have access to this command")
from unittest import TestCase
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Instructor import Instructor
from classes.TA import TA
from classes.Course import Course


class AssignTALab(TestCase):
        def setUp(self):
                self.TA1 = TA("TA1@uwm.edu", "TA1")
                self.Course1 = Course("CS101", 1)
                self.Course1.set_lab(1, 801)
                self.assertEqual(self.ui.command("assign_ta_course TA1@uwm.edu CS101"),
                                 "TA1@uwm.edu was assigned to CS101")

        def test_assign_ta_lab(self):
                # best case
                self.assertEqual(self.ui.command("assign_ta_lab TA1@uwm.edu 801"),
                                 "TA1@uwm.edu was assigned to lab 801")

        def test_assign_ta_lab_args_dne(self):
                # entered arguments that don't exist
                self.assertEqual(self.ui.command("assign_ta_lab TA1, 801"), "Error: invalid email address")
                self.assertEqual(self.ui.command("assign_ta_lab TA2@uwm.edu, 801"),
                                 "TA2@uwm.edu could not be assigned since it does not exist")
                self.assertEqual(self.ui.command("assign_ta_lab TA1@uwm.edu, 802"),
                                 "802 could not be assigned since it does not exist")

        def test_assign_ta_lab_num_args(self):
                # test number of arguments
                self.assertEqual(self.ui.command("assign_ta_lab TA@uwm.edu"), "Error: too few arguments")
                self.assertEqual(self.ui.command("assign_ta_lab"), "Error: too few arguments")

        def test_assign_ta_lab_full(self):
                # test if lab section already has a TA
                self.TA2 = ("TA2@uwm.edu", "TA2")
                self.assertEqual(self.ui.command("assign_ta_lab TA2@uwm.edu 801"),
                                 "Lab 801 already has been assigned a TA")

        def test_assign_ta_lab_not_ta(self):
                # test against non-TAs
                self.SUP = Supervisor("SUP@uwm.edu", "SUP")
                self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
                self.INS = Instructor("INS@uwm.edu", "INS")
                self.assertEqual(self.ui.command("assign_ta_lab INS@uwm.edu 801"), "Error: INS@uwm.edu is not a TA")
                self.assertEqual(self.ui.command("assign_ta_lab SUP@uwm.edu 801"), "Error: SUP@uwm.edu is not a TA")
                self.assertEqual(self.ui.command("assign_ta_lab ADMIN@uwm.edu 801"), "Error: ADMIN@uwm.edu is not a TA")
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
import unittest


class CreateCourseTests(unittest.TestCase):
    def setup(self):
        self.ui.command("create_user Administrator")
        self.ui.command("create_user Supervisor")

    """
    When the create course cmd is entered, it takes < 3 > arguments:
    - Title
    - Instructor
    - Open TA slots
    If Title and Instructor fields are filled in, create course is a success:
    - "Create course successful."
    If Title field is omitted, failure:
    - "Error creating course."
    If Instructor field is omitted, failure:
    - "Error creating course."
    If Title already exists, failure:
    - "Error creating  course."
    """
    def test_command_create_course_correct(self):
        self.assertEqual(self.ui.command("create_course Administrator"), "Create course successful.")
        self.assertEqual(self.ui.command("create_course Supervisor"), "Create course successful.")

    def test_command_create_course_no_title(self):
        self.assertEqual(self.ui.command("create_course Administrator"), "Error creating course.")
        self.assertEqual(self.ui.command("create_course Supervisor"), "Error creating course.")

    def test_command_create_course_no_instructor(self):
        self.assertEqual(self.ui.command("create_course Administrator"), "Error creating course.")
        self.assertEqual(self.ui.command("create_course Supervisor"), "Error creating course.")

    def test_command_create_course_already_exists(self):
        self.ui.command("create_course Administrator")
        self.assertEqual(self.ui.command("create_course Administrator"), "Error creating course")
        self.ui.command("create_course Supervisor")
        self.assertEqual(self.ui.command("create_course Supervisor"), "Error creating course")


class DeleteTests(unittest.TestCase):

    def setup(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")

    """
        When the delete command is entered, it takes one argument:
        - Username
        If the user has permission to delete and
        the username matches the database entry
        the user delete is successful:
        - "User deleted successfully"
        If the user does not have permission, failure:
        - "You do not have permission to delete users"
        If the username does not match or is omitted, failure:
        - "Error deleting account"
    """

    def test_delete_fromAdmin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("delete TA"), "User deleted successfully")

    def test_delete_fromSupervisor(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("delete TA"), "User deleted successfully")

    def test_delete_fromInstructor(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("delete TA"), "You do not have permission to delete users")

    def test_delete_fromTA(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("delete TA"), "You do not have permission to delete users")

    def test_delete_no_args(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("delete"), "Error deleting account")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("delete"), "Error deleting account")
        self.ui.command("logout")
        self.assertEqual(self.ui.command("delete"), "Error deleting account")

    def test_delete_wrongUsername(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("delete TA1@uwm.edu"), "Error deleting account")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("delete TA1@uwm.edu"), "Error deleting account")
        self.ui.command("logout")

import unittest
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA


class EditAccountTests(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")

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
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual("edit_account ADMN@uwm.edu password admn", "account edited")
        self.assertEqual(self.ADMIN.password, "admn")
        self.assertEqual("edit_account ADMN@uwm.edu username ADMN2@uwm.edu", "account edited")
        self.assertEqual(self.ADMIN.username, "ADMN2@uwm.edu")

    def test_edit_sup(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual("edit_account SUP@uwm.edu password admn", "account edited")
        self.assertEqual(self.SUP.password, "admn")
        self.assertEqual("edit_account SUP@uwm.edu username SUP2@uwm.edu", "account edited")
        self.assertEqual(self.SUP.username, "SUP2@uwm.edu")

    def test_edit_TA(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual("edit_account TA@uwm.edu password admn", "do not have permission to edit accounts")
        self.assertEqual("edit_account TA@uwm.edu username TA3@uwm.edu", "do not have permission to edit accounts")

    def test_edit_ins(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual("edit_account INS@uwm.edu password admn", "do not have permission to edit accounts")
        self.assertEqual("edit_account INS@uwm.edu username INS3@uwm.edu", "do not have permission to edit accounts")

    def test_edit_noargs(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual("edit_account  password admn", "invalid number of arguments")
        self.assertEqual("edit_account admn", "invalid number of arguments")
        self.assertEqual("edit_account", "invalid number of arguments")

    def test_edit_invalidargs(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual("edit_account ADMN@uwm.edu jajajaj admn", "invalid data to edit")
        self.assertEqual("edit_account ADMN@uwm.edu cs250 admn", "invalid data to edit")

import unittest
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA


class EditContactInfoTests(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")

    """
    both instructors and Ta's can edit their own contact information
    edit_contact_info takes 2 arguments 
        -type of info to update
        -new info
    if edit_contact_info successful
        -"contact info edited" displayed
    if edit_contact_info done by admin or supervisor
        -"contact info not edited"
    if number of args incorrect
        -"invalid number of arguments" displayed
    if type of info invalid
        -"invalid type of data to edit" displayed 
    """

    def test_eci_ins(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("edit_contact_info phone 111-111-1111"), "contact info edited")
        self.assertEqual(self.INS.phone_number, "111-111-1111")
        self.assertEqual(self.ui.command("edit_contact_info name John Tang Boyland"), "contact info edited")
        self.assertEqual(self.INS.name, "John Tang Boyland")

    def test_eci_ta(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("edit_contact_info phone 111-111-1111"), "contact info edited")
        self.assertEqual(self.TA.phone_number, "111-111-1111")
        self.assertEqual(self.ui.command("edit_contact_info name Fanglu Ju"), "contact info edited")
        self.assertEqual(self.TA.name, "Fanglu Ju")

    def test_eci_admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN ")
        self.assertEqual(self.ui.command("edit_contact_info phone 111-111-1111"), "contact info not edited")
        self.assertEqual(self.ui.command("edit_contact_info name Fanglu Ju"), "contact info not edited")

    def test_eci_sup(self):
        self.ui.command("login SUP@uwm.edu SUP ")
        self.assertEqual(self.ui.command("edit_contact_info phone 111-111-1111"), "contact info not edited")
        self.assertEqual(self.ui.command("edit_contact_info name Fanglu Ju"), "contact info not edited")

    def test_eci_invalid_number_args(self):
        self.ui.command("login TA@uwm.edu TA ")
        self.assertEqual(self.ui.command("edit_contact_info 111-111-1111"), "invalid number of arguments")
        self.assertEqual(self.ui.command("edit_contact_info name "), "invalid number of arguments")

    def test_eci_invalid_args(self):
        self.ui.command("login TA@uwm.edu TA ")
        self.assertEqual(self.ui.command("edit_contact_info stuff things"), "invalid info type to edit")
        self.assertEqual(self.ui.command("edit_contact_info username boom "), "invalid info type to edit")


import unittest


class EmailTests(unittest.TestCase):
    def setup(self):
        self.ui.command("create_user Admin AdminPassword")
        self.ui.command("create_user TA TAPassword")
        self.ui.command("create_user Student StuPassword")
        self.ui.command("create_user Supervisor SupPassword")
        self.ui.command("send_notification Message")

    """
        When the send notification command, it takes one parameter
        -the message to be sent
        if the message is sent successfully via email, send notification is a success
        -"Message sent successfully"
        If message is not sent, send notification failed
        -"Message not sent"
        if access is denied
        -"access denied"
    """
    def test_admin_user(self):
        self.ui.command(self.ui.command("login_Supervisor Sup SupPassword"), "login successful")
        self.ui.command(self.ui.command("send_notification Message"), "Access Denied")
        self.ui.command(self.ui.command("login_TA TA TAPassword"), "login successful")
        self.ui.command(self.ui.command("send_notification Message"), "Access Denied")
        self.ui.command(self.ui.command("login_Student Stu StuPassword"), "login successful")
        self.ui.command(self.ui.command("send_notification Message"), "Access Denied")

    def test_email_connected(self):
        self.assertEqual(self.ui.command("email Person"), "email not in system")
        self.assertEqual(self.ui.command("send_notification Message"), "Email not connected")

    def test_send_notification_correct(self):
        self.ui.command(self.ui.command("login_Admin Admin AdminPassword"), "login successful")
        self.assertEqual(self.ui.command("send_notification Message"), "Message sent successfully")

    def test_send_notification_fail(self):
        self.ui.command(self.ui.command("login_Admin Admin AdminPassword"), "login successful")
        self.assertEqual(self.ui.command("send_notification Message"), "Message not sent")

    def test_send_notification_no_message(self):
        self.assertEqual(self.ui.command("send_notification "), "No message to send")

import unittest
from classes.TA import TA
from classes.Instructor import Instructor
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator


class GetContactInfo(unittest.TestCase):
    def setUp(self):
        self.ADMIN = Administrator("admin@uwm.edu", "adminPass")
        self.ADMIN.change_name("Dave Brubeck")
        self.ADMIN.change_phone(4141234567)

        self.SUPER = Supervisor("super@uwm.edu", "superPass")
        self.SUPER.change_name("Donna Summer")
        self.SUPER.change_phone(4149876543)

        self.INSTR = Instructor("instr@uwm.edu", "instrPass")
        self.INSTR.change_name("Dean Martin")
        self.INSTR.change_phone(2621234567)

        self.T_AYY = TA("t_ayy@uwm.edu", "t_ayyPass")
        self.T_AYY.change_name("Daniel Craig")
        self.T_AYY.change_phone(2629876543)

    def test_get_info_admin(self):
        self.ui.command("Login admin@uwm.edu adminPass")
        self.assertEqual(self.ui.command("get_contact_info"),
                         "NAME           PHONE           EMAIL"
                         "Dave Brubeck   414.123.4567    admin@uwm.edu"
                         "Donna Summer   414.987.6543    super@uwm.edu"
                         "Dean Martin    262.123.4567    instr@uwm.edu"
                         "Daniel Craig   262.987.6543    t_ayy@uwm.edu")

    def test_get_info_super(self):
        self.ui.command("Login admin@uwm.edu adminPass")
        self.assertEqual(self.ui.command("get_contact_info"),
                         "NAME           PHONE           EMAIL"
                         "Dave Brubeck   414.123.4567    admin@uwm.edu"
                         "Donna Summer   414.987.6543    super@uwm.edu"
                         "Dean Martin    262.123.4567    instr@uwm.edu"
                         "Daniel Craig   262.987.6543    t_ayy@uwm.edu")

    def test_get_info_inst(self):
        self.ui.command("Login instr@uwm.edu instrPass")
        self.assertEqual(self.ui.command("get_contact_info"),
                         "NAME           PHONE           EMAIL"
                         "Dave Brubeck   414.123.4567    admin@uwm.edu"
                         "Donna Summer   414.987.6543    super@uwm.edu"
                         "Dean Martin    262.123.4567    instr@uwm.edu"
                         "Daniel Craig   262.987.6543    t_ayy@uwm.edu")

    def test_get_info_ta(self):
        self.ui.command("Login t_ayy@uwm.edu t_ayyPass")
        self.assertEqual(self.ui.command("get_contact_info"),
                         "NAME           PHONE           EMAIL"
                         "Dave Brubeck   414.123.4567    admin@uwm.edu"
                         "Donna Summer   414.987.6543    super@uwm.edu"
                         "Dean Martin    262.123.4567    instr@uwm.edu"
                         "Daniel Craig   262.987.6543    t_ayy@uwm.edu")


import unittest
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")
    """
    When a user wants to login two arguments are required
        -Username
        -password
    the password must match the password for the given username
    if login is successful
        -"login successful" displayed"
    if password is incorrect
        -"password invalid" displayed
    if username does not exist
        -"no such user" displayed
    """
    def test_valid_login_Admin(self):
        self.assertEqual(self.ui.command("Login ADMN@uwm.edu ADMN "), "login successful")

    def test_invalid_login_Admin(self):
        self.assertEqual(self.ui.command("Login ADMN@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login ADMN3@uwm.edu AdminPassword"), "No such user")

    def test_valid_login_TA(self):
        self.assertEqual(self.ui.command("Login TA@uwm.edu TA "), "login successful")

    def test_invalid_login_TA(self):
        self.assertEqual(self.ui.command("Login TA@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login TA2@uwm.edu TAPassword"), "No such user")

    def test_valid_login_Instructor(self):
        self.assertEqual(self.ui.command("Login INS@uwm.edu INS "), "login successful")

    def test_invalid_login_Instructor(self):
        self.assertEqual(self.ui.command("Login INS@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login INS2@uwm.edu InstructorPassword"), "No such user")

    def test_valid_login_Supervisor(self):
        self.assertEqual(self.ui.command("Login SUP@uwm.edu SUP "), "login successful")

    def test_invalid_login_Admin(self):
        self.assertEqual(self.ui.command("Login SUP@uwm.edu AdminPaword "), "Password invalid")
        self.assertEqual(self.ui.command("Login SUP2@uwm.edu SupervisorPassword"), "No such user")

    def test_invalid_number_args(self):
        self.assertEqual(self.ui.command("Login AdminPaword "), "invalid number of arguments")
        self.assertEqual(self.ui.command("Login SUP@uwm.edu "), "invalid number of arguments")

import unittest
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")
    """
    When a user wants to logout no arguments are required 
    if logout works properly
        -"logout successful"
    if logout does not work
        -"logout failed"
    """

    def test_logout_Admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_logout_TA(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_logout_Instructor(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_logout_Supervisor(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("logout"), "logout successful")

    def test_invalid_logout(self):
        self.assertEqual(self.ui.command("logout"), "logout failed")

#made by matt

import unittest

class ViewCourseAssignmentsTest(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")

    """
    an instructor has the ability to view what courses they are assigned to 
    view_course_assignments takes no arguments 
    if an instructor has no courses
        -"no courses assigned" is displayed"
    if an instructor has courses
        -each course is displayed linearly "course ta_slots"
    if an other type of user calls uses view_course_assignments
        -"access denied" is displayed 
    """

    def test_invalid_admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("view_course_assignments"), "access denied")

    def test_invalid_sup(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("view_course_assignments"), "access denied")

    def test_invalid_ta(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("view_course_assignments"), "access denied")

    def test_valid_ins(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_course_assignments"), "no courses assigned")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS361 3")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_course_assignments"), "CS361 3")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS351 3")
        self.ui.command("create_course INS@uwm.edu CS431 2")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_course_assignments"), "CS361 3 CS351 3 CS431 2")


import unittest
from classes.TA import TA
from classes.Instructor import Instructor
from classes.Supervisor import Supervisor
from classes.Administrator import Administrator
from classes.Course import Course


class ViewTAAssignmentsTest(unittest.TestCase):
    def setUp(self):
        self.SUP = Supervisor("SUP@uwm.edu", "SUP")
        self.ADMIN = Administrator("ADMN@uwm.edu", "ADMIN")
        self.INS = Instructor("INS@uwm.edu", "INS")
        self.TA = TA("TA@uwm.edu", "TA")
        self.TA = TA("TA1@uwm.edu", "TA1")
        self.TA = TA("TA2@uwm.edu", "TA2")
        self.Course1 = Course("CS351", 3)
        self.Course2 = Course("CS431", 2)
        self.Course3 = Course("CS361", 3)

    """
    A TA has the ability to view all TA course assignments
    view_ta_assignments takes no arguments

    if a TA calls it
        - List of each course and the TA(s) assigned to it

    if a Instructor calls it
        - List of each course and the TA(s) assigned to it

    if a admin or sup calls it
        - "access denied" is displayed

    if there are no courses
        -"no courses" is displayed

    if a course doesnt have a TA
        -"No TA" is displayed after the course
    """

    def test_invalid_admin(self):
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.assertEqual(self.ui.command("view_ta_assignments"), "access denied")

    def test_invalid_sup(self):
        self.ui.command("login SUP@uwm.edu SUP")
        self.assertEqual(self.ui.command("view_ta_assignments"), "access denied")

    def test_valid_ta(self):
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("view_ta_assignments"), "no courses")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS361 3")
        self.ui.command("logout")
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS351 3")
        self.ui.command("assign_ta_course TA@uwm.edu CS351 3")
        self.ui.command("create_course INS@uwm.edu CS431 2")
        self.ui.command("assign_ta_course TA@uwm.edu CS431 2")
        self.ui.command("assign_ta_course TA1@uwm.edu CS431 2")
        self.ui.command("logout")
        self.ui.command("login TA@uwm.edu TA")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA, CS351 3: TA, CS431 2: TA TA1")

    def test_valid_ins(self):
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_ta_assignments"), "no courses")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS361 3")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA")
        self.ui.command("logout")
        self.ui.command("login ADMN@uwm.edu ADMIN")
        self.ui.command("create_course INS@uwm.edu CS351 3")
        self.ui.command("assign_ta_course TA@uwm.edu CS351 3")
        self.ui.command("assign_ta_course TA1@uwm.edu CS351 2")
        self.ui.command("assign_ta_course TA2@uwm.edu CS351 2")
        self.ui.command("create_course INS@uwm.edu CS431 2")
        self.ui.command("assign_ta_course TA@uwm.edu CS431 2")
        self.ui.command("logout")
        self.ui.command("login INS@uwm.edu INS")
        self.assertEqual(self.ui.command("view_ta_assignments"), "CS361 3: No TA, CS351 3: TA TA1 TA2, CS431 2: TA")