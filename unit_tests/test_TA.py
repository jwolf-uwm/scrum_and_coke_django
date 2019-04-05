# created by Dillan

from django.test import TestCase
from classes.Person import Person
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA
from ta_assign import models
from classes.Course import Course


class TestTA(TestCase):

    def setUp(self):
        self.ta1 = TA("ta1@uwm.edu", "password", "ta")
        self.course1 = Course("CS101", 0)
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_ta_course1 = models.ModelTACourse()
        mod_ta_course1.course = mod_course1
        mod_ta1 = models.ModelPerson.objects.get(email="ta1@uwm.edu")
        mod_ta_course1.TA = mod_ta1
        mod_ta_course1.save()

    def test_view_ta_assignments(self):
        self.assertEqual(self.ta1.view_ta_assignments()[0], "Course: CS101 TA: DEFAULT, ta1@uwm.edu")

    def test_read_public_contact(self):
        # self.assertEqual(self.ta1.read_public_contact(self.class_list))
        pass

    models.ModelPerson.objects.all().delete()
