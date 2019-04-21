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



