# created by Matt

from classes.Administrator import Administrator
from unittest import TestCase


class TestAdministrator(TestCase):
    def setUp(self):
        self.ad1 = Administrator("ad1@uwm.edu", "ad1pass")

    def test_create_course(self):
        self.assertTrue(self.ad1.create_course("CS361", 3))
        self.course1 = ("CS337", 1)
        # course already exists
        self.assertFalse(self.ad1.create_course("CS337", 2))

    def test_create_account(self):
        self.assertTrue(self.ad1.create_account("DustyBottoms@uwm.edu", "better_password"))
        self.ad2 = Administrator("ad2@uwm.edu", "ad2pass")
        # taken email
        self.assertFalse(self.ad1.create_account("ad2@uwm.edu", "new_pass"))
        # taken password
        self.assertFalse(self.ad1.create_account("George_Likes_Beef@uwm.edu", "better_password"))

    def test_edit_account(self):
        self.random_user = ("rando@uwm.edu", "im_random", 1234567, "Jerry Seinfeld")

        # test edit password
        self.ad1.edit_account("rando@uwm.edu", "password", "new_pass")
        self.assertEqual(self.random_user[2], "new_pass")

        # test edit email
        self.ad1.edit_account("rando@uwm.edu", "email", "NEW_EMAIL@uwm.edu")
        self.assertEqual(self.random_user[1], "NEW_EMAIL@uwm.edu")

        # test edit phone
        self.ad1.edit_account("rando@uwm.edu", "phone", 3456789)
        self.assertEqual(self.random_user[3], 3456789)

        # test edit name
        self.ad1.edit_account("rando@uwm.edu", "name", "Howard Stern")
        self.assertEqual(self.random_user[4], "Howard Stern")

        self.assertFalse(self.ad1.edit_account("rando@uwm.edu", "password"))
        self.assertFalse(self.ad1.edit_account("rando@uwm.edu"))
        self.assertFalse(self.ad1.edit_account("wrong_email@uwm.edu", "password", "new_pass"))
        self.assertFalse(self.ad1.edit_account("rando@uwm.edu", "wrong_field", "new_pass"))
        self.assertFalse(self.ad1.edit_account("rando@uwm.edu", "password", ";\"π  /\\# bad `  pass ' chars"))

    def test_delete_account(self):
        self.deleted_user = ("delete_me@uwm.edu", "delete_me_pass")
        self.ad1.delete_account("delete_me@uwm.edu")
        self.copy_user = ("delete_me@uwm.edu", "delete_me_pass")
        self.assertNotEqual(self.copy_user, self.deleted_user)

    def test_send_notification(self):
        self.assertTrue(self.ad1.send_notification("I Like To Eat French Fries In The Rain"))

    def test_access_info(self):
        # creating stuff in the system
        self.user = ("email@uwm.edu", "pass")
        self.system_stuff = ([self.ad1, self.ad2, self.user],
                            ["ad1@uwm.edu", "ad2@uwm.edu", "email@uwm.edu"],
                            ["ad1pass", "ad2pass", "pass"])
        self.assertEqual(self.ad1.access_info(), self.system_stuff)

from unittest import TestCase
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

# created by Jeff

from classes.Instructor import Instructor
from unittest import TestCase


class TestInstructor(TestCase):

    def setup(self):
        self.instructor1 = Instructor("instructor1@uwm.edu", "DEFAULT_PASSWORD")
        self.instructor2 = Instructor("instructor2@uwm.edu", "DEFAULT_PASSWORD")
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

# created by Grant

from unittest import TestCase
from classes.Person import Person


class TestPerson(TestCase):

    def setup(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD")
        self.person2 = Person("person2@uwm.edu", "DEFAULT_PASSWORD")

    def test_init_(self):
        self.assertEquals(self.person1.email, "person1@uwm.edu")
        self.assertEquals(self.person1.password, "DEFAULT_PASSWORD")
        self.assertEquals(self.person1.name, "DEFAULT")
        self.assertEquals(self.person1.phone_number, 0000000000)

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

# created by Dillan

from unittest import TestCase
from classes.TA import TA


class TestTA(TestCase):

    def setup(self):
        self.ta1 = TA("DEFAULT_EMAIL@uwm.edu", "DEFAULT_PASSWORD")
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
