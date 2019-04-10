# created by Jeff

from django.test import TestCase
from classes.Person import Person
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA
from ta_assign import models
from classes.Course import Course


class TestInstructor(TestCase):

    def setUp(self):
        # self.instructor1 = Instructor("instructor1@uwm.edu", "DEFAULT_PASSWORD")
        # self.instructor2 = Instructor("instructor2@uwm.edu", "DEFAULT_PASSWORD")
        # fake TA
        # self.ta1 = ("ta1@uwm.edu", "DEFAULT_PASSWORD")
        # self.ta2 = ("ta2@uwm.edu", "DEFAULT_PASSWORD")
        # fake Course
        # self.course1 = ("Course 1", 2, self.instructor1, [self.ta1])
        # self.course2 = ("Course 2", 2, self.instructor2, [self.ta2])
        self.inst0 = Instructor("inst0@uwm.edu", "password", "instructor")
        self.ta0 = TA("ta0@uwm.edu", "password", "ta")
        self.ta1 = TA("ta1@uwm.edu", "password", "ta")
        self.ta2 = TA("ta2@uwm.edu", "password", "ta")
        self.ta3 = TA("ta3@uwm.edu", "password", "ta")
        self.course1 = Course("CS101", 0)
        self.course2 = Course("CS201", 0)
        self.course3 = Course("CS301", 0)

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

    def test_view_ta_assign1(self):
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_ta_course1 = models.ModelTACourse()
        mod_ta_course1.course = mod_course1
        mod_ta1 = models.ModelPerson.objects.get(email="ta1@uwm.edu")
        mod_ta_course1.TA = mod_ta1
        mod_ta_course1.save()
        self.assertEqual(self.inst0.view_ta_assign()[0], "Course: CS101 TA: DEFAULT, ta1@uwm.edu")

    def test_view_ta_assign2(self):
        mod_course2 = models.ModelCourse.objects.get(course_id="CS201")
        mod_ta_course2 = models.ModelTACourse()
        mod_ta_course2.course = mod_course2
        mod_ta2 = models.ModelPerson.objects.get(email="ta2@uwm.edu")
        mod_ta_course2.TA = mod_ta2
        mod_ta_course2.save()
        self.assertEqual(self.inst0.view_ta_assign()[0], "Course: CS201 TA: DEFAULT, ta2@uwm.edu")

    def test_view_ta_assign3(self):
        mod_course3 = models.ModelCourse.objects.get(course_id="CS301")
        mod_ta_course3 = models.ModelTACourse()
        mod_ta_course3.course = mod_course3
        mod_ta3 = models.ModelPerson.objects.get(email="ta3@uwm.edu")
        mod_ta_course3.TA = mod_ta3
        mod_ta_course3.save()
        self.assertEqual(self.inst0.view_ta_assign()[0], "Course: CS301 TA: DEFAULT, ta3@uwm.edu")

    def test_view_ta_assign4(self):
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
        self.assertEqual(self.inst0.view_ta_assign()[0], "Course: CS101 TA: DEFAULT, ta1@uwm.edu")
        self.assertEqual(self.inst0.view_ta_assign()[1], "Course: CS201 TA: DEFAULT, ta2@uwm.edu")
        self.assertEqual(self.inst0.view_ta_assign()[2], "Course: CS301 TA: DEFAULT, ta3@uwm.edu")
        self.assertEqual(self.inst0.view_ta_assign(), ['Course: CS101 TA: DEFAULT, ta1@uwm.edu',
                                                       'Course: CS201 TA: DEFAULT, ta2@uwm.edu',
                                                       'Course: CS301 TA: DEFAULT, ta3@uwm.edu'])

