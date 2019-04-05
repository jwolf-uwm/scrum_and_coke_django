# created by Jeff

from classes.Instructor import Instructor
from django.test import TestCase
from ta_assign import models


class TestInstructor(TestCase):

    instructor1 = Instructor("instructor1@uwm.edu", "DEFAULT_PASSWORD", "instructor")
    instructor2 = Instructor("instructor2@uwm.edu", "DEFAULT_PASSWORD", "instructor")

    def setup(self):
        # self.instructor1 = Instructor("instructor1@uwm.edu", "DEFAULT_PASSWORD")
        # self.instructor2 = Instructor("instructor2@uwm.edu", "DEFAULT_PASSWORD")
        # fake TA
        self.ta1 = ("ta1@uwm.edu", "DEFAULT_PASSWORD")
        self.ta2 = ("ta2@uwm.edu", "DEFAULT_PASSWORD")
        # fake Course
        self.course1 = ("Course 1", 2, self.instructor1, [self.ta1])
        self.course2 = ("Course 2", 2, self.instructor2, [self.ta2])

    def test___init__(self):
        self.assertEquals(self.instructor1.email, "DEFAULT_EMAIL")
        self.assertEquals(self.instructor1.password, "DEFAULT_PASSWORD")
        self.assertEquals(self.instructor1.name, "DEFAULT")
        self.assertEquals(self.instructor1.phone_number, "DEFAULT")

    def test_edit_contact(self):
        # still using instructor1
        self.instructor1.edit_contact_info("name", "Bob Ross")
        self.assertNotEquals(self.instructor1.name, "DEFAULT")
        self.assertEquals(self.instructor1.name, "Bob Ross")

        self.instructor1.edit_contact_info("phone", "4145459999")
        self.assertNotEquals(self.instructor1.phone_number, "0000000000")
        self.assertEquals(self.instructor1.phone_number, "4145459999")

        self.instructor1.edit_contact_info("email", "bob_ross@uwm.edu")
        self.assertNotEquals(self.instructor1.email, "instructor1@uwm.edu")
        self.assertEquals(self.instructor1.email, "bob_ross@uwm.edu")

        with self.assertRaises(TypeError):
            self.instructor1.edit_contact_info(2, "Ted")

        with self.assertRaises(TypeError):
            self.instructor1.edit_contact_info("name", 41.6)

    def test_read_public_contact(self):
        self.assertNotEquals(self.instructor1.read_public_contact(), "DEFAULT, instructor1@uwm1.edu")
        self.assertEquals(self.instructor1.read_public_contact(), "Bob Ross, bob_ross@uwm.edu")

    def test_send_notification_ta(self):
        self.assertTrue(self.instructor1.send_notification_ta("Hi!"))

    def test_view_course(self):
        self.assertEquals(self.instructor1.view_course_assign(), "Course 1")
        self.assertNotEquals(self.instructor1.view_course_assign(), "Course 2")

    def test_view_ta_assign(self):
        self.assertEquals(self.instructor1.view_ta_assign()[0], self.ta1)
        self.assertNotEquals(self.instructor1.view_ta_assign(), self.ta2)

    models.ModelPerson.objects.all().delete()
