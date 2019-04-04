# created by Grant

from django.test import TestCase
from classes.Person import Person
from ta_assign import models


class TestPerson(TestCase):
    person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "person")
    person2 = Person("person2@uwm.edu", "DEFAULT_PASSWORD", "person")

    def test_init_(self):
        # self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD")
        # self.person2 = Person("person2@uwm.edu", "DEFAULT_PASSWORD")
        self.assertEquals(self.person1.email, "person1@uwm.edu")
        self.assertEquals(self.person1.password, "DEFAULT_PASSWORD")
        # self.assertEquals(self.person1.name, "DEFAULT")
        # self.assertEquals(self.person1.phone_number, 0000000000)

    def test_change_password(self):
        self.assertTrue(self.person1.change_password("DEFAULT_PASSWORD", "password"))
        self.assertEquals(self.person1.password, "password")
        self.assertNotEquals(self.person1.password, "DEFAULT_PASSWORD")
        self.assertFalse(self.person1.change_password("DEFAULT_PASSWORD", "some_password"))

    def test_change_email(self):
        self.person1.change_email("snoop@uwm.edu")
        self.assertEquals(self.person1.email, "snoop@uwm.edu")
        self.assertNotEquals(self.person1.email, "person1@uwm.edu")

        with self.assertRaises(ValueError):
            self.person1.change_email("snoop@gmail.com")

        with self.assertRaises(ValueError):
            self.person1.change_email("no_at_symbol_or_dot_something")

    def test_change_phone(self):
        self.person1.change_phone(4144244343)
        self.assertEquals(self.person1.phone_number, 4144244343)
        self.assertNotEquals(self.person1.phone_number, 0000000000)

    def test_change_name(self):
        self.person1.change_name("Snoop Doggy Dog")
        self.assertEquals(self.person1.name, "Snoop Doggy Dog")
        self.assertNotEquals(self.person1.name, "DEFAULT")

    def test_get_contact_info(self):
        self.assertEquals(self.person1.get_contact_info(), "Snoop Doggy Dog, snoop@uwm.edu, 4144244343")
        self.assertNotEquals(self.person1.get_contact_info(), "DEFAULT, person1@uwm.edu, 0000000000")

    def test_login(self):
        self.assertEquals(self.person1.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Invalid login info.")
        self.assertEquals(self.person1.login("snoop@uwm.edu", "password"), "Login successful.")

    def test_logout(self):
        self.assertTrue(self.person1.logout())

    # careful, this will delete all people in the database to cleanup
    # disable if there's something you need to persist
    models.ModelPerson.objects.all().delete()
