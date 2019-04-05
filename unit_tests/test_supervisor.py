# created by Evan

from django.test import TestCase
from classes.Supervisor import Supervisor
from ta_assign import models
from classes.Course import Course
from classes.Instructor import Instructor
from classes.TA import TA
from classes.Administrator import Administrator


class TestSupervisor(TestCase):

    def setUp(self):
        self.sup = Supervisor("sup@uwm.edu", "sup_pass", "Supervisor")

    def test_assign_instructor_course(self):
        # fake instructors
        self.ins1 = Instructor("ins1@uwm.edu", "blah", "instructor")
        self.ins2 = Instructor("ins2@uwm.edu", "inspass", "instructor")
        # fake course
        self.course1 = Course("CS101", 2)
        self.course2 = Course("CS202", 0)
        # instructor 1 is assigned CS101
        self.assertTrue(self.sup.assign_instructor(self.ins1, self.course1))
        # self.assertEqual(self.ins1.courses[0], self.course1)
        self.assertEqual(self.course1.instructor.email, "ins1@uwm.edu")

        # assign instructor 1 another course
        self.assertTrue(self.sup.assign_instructor(self.ins1, self.course2))
        # self.assertEqual(self.ins1.courses[1], self.course2)
        self.assertEqual(self.course2.instructor.email, "ins1@uwm.edu")

        # instructor 2 is assigned CS101
        self.assertTrue(self.sup.assign_instructor(self.ins2, self.course1))
        # self.assertEqual(self.ins2.courses[0], self.course1)
        self.assertEqual(self.course1.instructor.email, "ins2@uwm.edu")
        # self.assertNotEqual(self.ins1.courses[0], self.course1)

        self.ta1 = TA("ta1@uwm.edu", "beh", "TA")
        with self.assertRaises(TypeError):
            self.sup.assign_instructor(self.ta1, self.course1)

        self.admin1 = Administrator("admin@uwm.edu", "admin1", "Administrator")
        with self.assertRaises(TypeError):
            self.sup.assign_instructor(self.admin1, self.course1)

        with self.assertRaises(TypeError):
            self.sup.assign_instructor(self.sup, self.course1)

        self.sup.create_course("CS337-401", 3)
        da_course = models.ModelCourse.objects.get(course_id="CS337-401")
        # self.test_course = Course(da_course.course_id, da_course.num_labs)
        # self.sup.assign_instructor(self.ins1, self.test_course)
        da_courseaa = models.ModelCourse.objects.get(course_id="CS337-401")
        self.assertEquals(da_courseaa.num_labs, da_course.num_labs)
        self.assertEquals(da_courseaa.course_id, da_course.course_id)
        # self.assertEquals(da_courseaa.instructor, self.ins1.email)

    def test_assign_ta_course(self):
        # TA 1 is assigned CS101
        # fake instructors
        self.ta1 = Instructor("ta1@uwm.edu", "blah", "TA")
        self.ta2 = Instructor("ta2@uwm.edu", "inspass", "TA")
        # fake course
        self.course1 = Course("CS101", 2)
        self.course2 = Course("CS202", 0)
        # instructor 1 is assigned CS101
        self.sup.assign_ta_course(self.ta1, self.course1[0])
        self.assertEqual(self.ta1_course, "CS101")
        self.assertEqual(self.course1_tas[0], "ta1@uwm.edu")

        # assign TA 1 another course
        self.sup.assign_ta_course(self.ta1, self.course2[0])
        self.assertEqual(self.ta1_course, "CS202")
        self.assertEqual(self.course2_tas[0], "ta1@uwm.edu")

        # TA 2 is assigned CS101
        self.sup.assign_ta_course(self.ta2, self.course1[0])
        self.assertEqual(self.ta2_course, "CS101")
        self.assertEqual(self.course1_tas[1], "ins2@uwm.edu")
        self.assertEqual(self.course1_tas[0], "ins1@uwm.edu")

        # Try to assign a third TA to CS101
        self.sup.assign_ta_course(self.ta3, self.course1[0])
        self.assertNotEqual(self.ta3_course, "CS101")
        self.assertNotEqual(self.course1_tas[2], "ins3@uwm.edu")

        self.assertRaises(self.sup.assign_ta_course(self.ins1, self.course1[0]), TypeError)

    def test_assign_ta_lab(self):
        # TA 1 is assigned CS101 - 801
        self.sup.assign_ta_lab(self.ta1, "CS101", 801)
        self.assertEqual(self.ta1_sections[0], 801)

        # TA 2 is assigned CS101 - 802
        self.sup.assign_ta_lab(self.ta2, 802)
        self.assertEqual(self.ta2_sections[0], "CS101")

        # Try to assign TA 1 another lab section
        self.assertRaises(self.sup.assign_ta_lab(self.ta1, self.course2[0]), OverflowError)

        self.assertRaises(self.sup.assign_ta_lab(self.ins1, self.course1[0]), TypeError)
