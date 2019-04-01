# created by Matt
from django.test import TestCase
from classes.Administrator import Administrator
from classes.Instructor import Instructor
from classes.TA import TA
from ta_assign import models
# from classes.Course import Course
# from classes.Database import Database


class TestAdministrator(TestCase):

    # def setUp(self):
        # self.ad1 = Administrator("ad1@uwm.edu", "ad1pass")
        # self.data = Database()
        # pass

    def test_create_course(self):
        # self.assertEqual(self.ad1.create_course("CS361", 3), Course("CS361", 3))
        # self.data.courses.append(self, Course("CS337", 1))
        # course already exists
        self.assertEqual(self.ad1.create_course("CS337", 2), "Course already exists")

    def test_create_account(self):
        # Jeff's tests

        # setup admin
        self.ad1 = Administrator("ad1@uwm.edu", "ad1pass")

        # BEGIN CREATE INSTRUCTOR TESTS
        # create unused instructor account
        self.assertTrue(self.ad1.create_account("DustyBottoms@uwm.edu", "better_password", "instructor"))
        # get account that was just setup
        test_model_ins = models.ModelInstructor.objects.get(email="DustyBottoms@uwm.edu")
        # make sure email is equal
        self.assertEqual(test_model_ins.email, "DustyBottoms@uwm.edu")
        # make sure password is equal
        self.assertEqual(test_model_ins.password, "better_password")
        # default name test
        self.assertEqual(test_model_ins.name, "DEFAULT")
        # default phone test
        self.assertEqual(test_model_ins.phone, -1)
        # login false test
        self.assertFalse(test_model_ins.isLoggedOn)
        # END CREATE INSTRUCTOR TESTS

        # BEGIN CREATE TA TESTS

        # END CREATE TA TESTS

        self.instructor2 = Instructor("ad2@uwm.edu", "ad2pass")
        # taken email
        self.assertFalse(self.ad1.create_account("ad2@uwm.edu", "new_pass", "instructor"))
        # taken password
        # I'm not sure that we should care if two or more people pick the same password - Jeff
        # self.assertFalse(self.ad1.create_account("George_Likes_Beef@uwm.edu", "better_password"))

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

    # models.ModelPerson.objects.all().delete()
