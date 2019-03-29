# created by Evan

from unittest import TestCase
from classes.Supervisor import Supervisor


class TestSupervisor(TestCase):
    def setUp(self):
        self.sup = Supervisor("sup@uwm.edu", "sup_pass")

        # fake instructors
        self.ins1_courses = []
        self.ins1 = "ins1@uwm.edu"
        self.ins2_courses = []
        self.ins2 = "in2s@uwm.edu"
        # fake course
        self.course1_tas = []
        self.course1_instructor = ""
        self.course1 = ("CS101", 2)
        self.course2_tas = []
        self.course2_instructor = ""
        self.course2 = ("CS202", 0)
        # fake ta
        self.ta1_sections = []
        self.ta1_course = ""
        self.ta1 = "ta1@uwm.edu"
        self.ta2_sections = []
        self.ta2_course = ""
        self.ta2 = "ta2@uwm.edu"
        self.ta3 = "ta3.uwm.edu"
        self.ta3_course = ""

    def test_assign_instructor_course(self):
        # instructor 1 is assigned CS101
        self.sup.assign_instructor(self.ins1, self.course1[0])
        self.assertEqual(self.ins1_courses[0], "CS101")
        self.assertEqual(self.course1_instructor, "ins1@uwm.edu")

        # assign instructor 1 another course
        self.sup.assign_instructor(self.ins1, self.course2[0])
        self.assertEqual(self.ins1_courses[1], "CS202")
        self.assertEqual(self.course2_instructor, "ins1@uwm.edu")

        # instructor 2 is assigned CS101
        self.sup.assign_instructor(self.ins2, self.course1[0])
        self.assertEqual(self.ins2_courses[0], "CS101")
        self.assertEqual(self.course1_instructor, "ins2@uwm.edu")
        self.assertNotEqual(self.ins1_courses[0], "CS101")

        self.assertRaises(self.sup.assign_instructor(self.ta1, self.course1[0]), TypeError)

    def test_assign_ta_course(self):
        # TA 1 is assigned CS101
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
