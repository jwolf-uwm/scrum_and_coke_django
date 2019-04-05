# created by Grant

from django.test import TestCase
from classes.Person import Person
from ta_assign import models


class TestPerson(TestCase):

    def test_init_(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(self.person1.email, "person1@uwm.edu")
        self.assertEquals(self.person1.password, "DEFAULT_PASSWORD")

    def test_change_password(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertTrue(self.person1.change_password("password"))
        self.assertEquals(self.person1.password, "password")
        self.assertNotEquals(self.person1.password, "DEFAULT_PASSWORD")

    def test_change_email(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_email("snoop@uwm.edu")
        self.assertEquals(self.person1.email, "snoop@uwm.edu")
        self.assertNotEquals(self.person1.email, "person1@uwm.edu")
        self.assertFalse(self.person1.change_email("snoop@gmail.com"))
        self.assertFalse(self.person1.change_email("no_at_symbol_or_dot_something"))

    def test_change_phone(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_phone(4144244343)
        self.assertEquals(self.person1.phone_number, 4144244343)
        self.assertNotEquals(self.person1.phone_number, 0000000000)

    def test_change_name(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_name("Snoop Doggy Dog")
        self.assertEquals(self.person1.name, "Snoop Doggy Dog")
        self.assertNotEquals(self.person1.name, "DEFAULT")

    def test_get_contact_info(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(self.person1.get_contact_info(), "Snoop Doggy Dog, snoop@uwm.edu, 4144244343")
        self.assertNotEquals(self.person1.get_contact_info(), "DEFAULT, person1@uwm.edu, 0000000000")

    def test_login(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(Person.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertTrue(model_person1.isLoggedOn)
        self.assertEquals(Person.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "User already logged in")
        self.assertEquals(Person.login("snoop@uwm.edu", "password"), "Invalid login info")

    def test_logout(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(Person.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")
        self.assertTrue(self.person1.logout())