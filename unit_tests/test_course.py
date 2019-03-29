from django.test import TestCase
from classes.Course import Course


class TestCourse(TestCase):

    def setup(self):
        self.course1 = Course("CS251", 2)
        self.course2 = Course("CS535", 0)
        # fake instructor
        self.instructor1 = "Professor Professorson"
        # fake TAs
        self.ta1 = "Tommy Adams"
        self.ta2 = "Tanya Anderson"
        self.ta3 = "Tina Abbot"

    def test___init__(self):
        self.assertEquals(self.course1.course_id, "CS251")
        self.assertEquals(self.course1.num_labs, 2)
        self.assertEquals(self.course1.instructor, "Dr. Default")
        self.assertEquals(self.course1.tee_ays, [])

    def test_set_course_id(self):
        self.course1.set_course_id("CS351")
        self.assertEquals(self.course1.course_id, "CS351")
        self.assertNotEquals(self.course1.course_id, "CS251")

    def test_set_instructor(self):
        # this needs to use
        self.course1.set_instructor("Professor Professorson")
        self.assertEquals(self.course1.instructor, self.instructor1)
        self.assertNotEquals(self.course1.instructor, "Dr. Default")

    def test_set_num_labs(self):
        self.course1.set_num_labs(4)
        self.assertEquals(self.course1.num_labs, 4)
        self.assertNotEquals(self.course1.num_labs, 2)

    def test_add_tee_ay(self):
        self.course1.add_tee_ay(self.ta1)
        self.course1.add_tee_ay(self.ta2)
        self.course2.add_tee_ay(self.ta3)
        self.assertEquals(self.course1.tee_ays[0], self.ta1)
        self.assertEquals(self.course1.tee_ays[0], self.ta2)
        self.assertEquals(self.course2.tee_ays[0], self.ta3)
        self.assertNotEquals(self.course1.tee_ays, [])
        self.assertNotEquals(self.course2.tee_ays, [])

    def test_get_course_id(self):
        self.assertEquals(self.course1.get_course_id(), "CS351")
        self.assertNotEquals(self.course1.get_course_id(), "CS251")

    def test_get_num_labs(self):
        self.assertEquals(self.course1.get_num_labs(), 4)
        self.assertNotEquals(self.course1.get_num_labs(), 2)

    def test_get_tee_ays(self):
        self.assertEquals(self.course1.get_tee_ays(), [self.ta1, self.ta2])
        self.assertEquals(self.course2.get_tee_ays(), [self.ta3])
        self.assertNotEquals(self.course1.get_tee_ays(), [])
        self.assertNotEquals(self.course2.get_tee_ays(), [])
