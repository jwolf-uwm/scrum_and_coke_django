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
        self.ta0 = TA("ta0@uwm.edu", "password", "ta")
        self.ta1 = TA("ta1@uwm.edu", "password", "ta")
        self.ta2 = TA("ta2@uwm.edu", "password", "ta")
        self.ta3 = TA("ta3@uwm.edu", "password", "ta")
        self.course1 = Course("CS101", 0)
        self.course2 = Course("CS201", 0)
        self.course3 = Course("CS301", 0)

    def test_view_ta_assignments1(self):
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_ta_course1 = models.ModelTACourse()
        mod_ta_course1.course = mod_course1
        mod_ta1 = models.ModelPerson.objects.get(email="ta1@uwm.edu")
        mod_ta_course1.TA = mod_ta1
        mod_ta_course1.save()
        self.assertEqual(self.ta1.view_ta_assignments()[0], "Course: CS101 TA: DEFAULT, ta1@uwm.edu")

    def test_view_ta_assignments2(self):
        mod_course2 = models.ModelCourse.objects.get(course_id="CS201")
        mod_ta_course2 = models.ModelTACourse()
        mod_ta_course2.course = mod_course2
        mod_ta2 = models.ModelPerson.objects.get(email="ta2@uwm.edu")
        mod_ta_course2.TA = mod_ta2
        mod_ta_course2.save()
        self.assertEqual(self.ta2.view_ta_assignments()[0], "Course: CS201 TA: DEFAULT, ta2@uwm.edu")

    def test_view_ta_assignments3(self):
        mod_course3 = models.ModelCourse.objects.get(course_id="CS301")
        mod_ta_course3 = models.ModelTACourse()
        mod_ta_course3.course = mod_course3
        mod_ta3 = models.ModelPerson.objects.get(email="ta3@uwm.edu")
        mod_ta_course3.TA = mod_ta3
        mod_ta_course3.save()
        self.assertEqual(self.ta3.view_ta_assignments()[0], "Course: CS301 TA: DEFAULT, ta3@uwm.edu")

    def test_view_ta_assignments4(self):
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_ta_course1 = models.ModelTACourse()
        mod_ta_course1.course = mod_course1
        mod_ta1 = models.ModelPerson.objects.get(email="ta1@uwm.edu")
        mod_ta_course1.TA = mod_ta1
        mod_ta_course1.save()
        mod_course2 = models.ModelCourse.objects.get(course_id="CS201")
        mod_ta_course2 = models.ModelTACourse()
        mod_ta_course2.course = mod_course2
        mod_ta2 = models.ModelPerson.objects.get(email="ta2@uwm.edu")
        mod_ta_course2.TA = mod_ta2
        mod_ta_course2.save()
        mod_course3 = models.ModelCourse.objects.get(course_id="CS301")
        mod_ta_course3 = models.ModelTACourse()
        mod_ta_course3.course = mod_course3
        mod_ta3 = models.ModelPerson.objects.get(email="ta3@uwm.edu")
        mod_ta_course3.TA = mod_ta3
        mod_ta_course3.save()
        self.assertEqual(self.ta0.view_ta_assignments()[0], "Course: CS101 TA: DEFAULT, ta1@uwm.edu")
        self.assertEqual(self.ta0.view_ta_assignments()[1], "Course: CS201 TA: DEFAULT, ta2@uwm.edu")
        self.assertEqual(self.ta0.view_ta_assignments()[2], "Course: CS301 TA: DEFAULT, ta3@uwm.edu")
        self.assertEqual(self.ta0.view_ta_assignments(), ['Course: CS101 TA: DEFAULT, ta1@uwm.edu',
                                                          'Course: CS201 TA: DEFAULT, ta2@uwm.edu',
                                                          'Course: CS301 TA: DEFAULT, ta3@uwm.edu'])

    def test_read_public_contact(self):
        # self.assertEqual(self.ta1.read_public_contact(self.class_list))
        pass
