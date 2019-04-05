# created by Dillan

from django.test import TestCase
from classes.TA import TA
from ta_assign import models


class TestTA(TestCase):

    ta1 = TA("DEFAULT_EMAIL@uwm.edu", "DEFAULT_PASSWORD", "ta")

    def setup(self):
        # self.ta1 = TA("DEFAULT_EMAIL@uwm.edu", "DEFAULT_PASSWORD")
        self.instructor1 = ("DEFAULT_EMAIL@uwm.edu", "DEFAULT_PASSWORD")
        self.instructor2 = ("DEFAULT_EMAIL@uwm.edu", "DEFAULT_PASSWORD")
        self.instructor3 = ("DEFAULT_EMAIL@uwm.edu", "DEFAULT_PASSWORD")
        self.course1 = ("DEFAULT_ID", 101, self.instructor1, [])
        self.course_catalog = (("DEFAULT_ID1", 101, self.instructor1, [self.ta1]),
                              ("DEFAULT_ID2", 101, self.instructor1, []),
                              ("DEFAULT_ID3", 101, self.instructor1, [self.ta1]),
                              ("DEFAULT_ID4", 101, self.instructor1, []))
        self.class_list = (self.instructor1, self.instructor2, self.instructor3, self.ta1)

    def test_view_ta_assignments(self):
        self.assertEqual(self.ta1.view_ta_assignment(self.course_catalog), ["DEFAULT_ID1", "DEFAULT_ID3"])

    def test_read_public_contact(self):
        self.assertEqual(self.ta1.read_public_contact(self.class_list))

    models.ModelPerson.objects.all().delete()
