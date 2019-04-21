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
