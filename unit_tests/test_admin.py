# created by Matt
from django.test import TestCase
from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA
from ta_assign import models
from classes.Course import Course
# from classes.Database import Database


class TestAdministrator(TestCase):

    # We likely don't need this anymore, because best I can figure it doesn't work well with django - Jeff
    # def setUp(self):
        # self.ad1 = Administrator("ad1@uwm.edu", "ad1pass")
        # self.data = Database()
        # pass

    def setUp(self):
        self.ad1 = Administrator("ad1@uwm.edu", "ad1pass", "administrator")

    def test_create_course(self):
        # setup admin
        self.ad1 = Administrator("ad1@uwm.edu", "ad1pass", "administrator")
        # setup supervisor
        self.sup1 = Supervisor("sup1@uwm.edu", "sup1pass", "supervisor")

        # create a new course as admin
        self.assertTrue(self.ad1.create_course("CS361-401", 3))
        # get the added course from the db
        da_course = models.ModelCourse.objects.get(course_id="CS361-401")
        # make sure found course is the same
        self.assertEqual(da_course.course_id, "CS361-401")
        self.assertEqual(da_course.num_labs, 3)
        self.assertEqual(da_course.instructor, "not_set@uwm.edu")

        # create a new course as supervisor
        self.assertTrue(self.sup1.create_course("CS251-401", 3))
        # get the added course from the db
        da_course = models.ModelCourse.objects.get(course_id="CS251-401")
        # make sure found course is the same
        self.assertEqual(da_course.course_id, "CS251-401")
        self.assertEqual(da_course.num_labs, 3)
        self.assertEqual(da_course.instructor, "not_set@uwm.edu")

        # create the same course again with no changes
        self.assertFalse(self.ad1.create_course("CS361-401", 3))
        # create the same course with a different number of labs
        self.assertFalse(self.ad1.create_course("CS361-401", 2))
        # create teh same course with a different section number (technically a new course)
        self.assertTrue(self.ad1.create_course("CS361-402", 3))
        da_course = models.ModelCourse.objects.get(course_id="CS361-402")
        # make sure found course is the same
        self.assertEqual(da_course.course_id, "CS361-402")
        self.assertEqual(da_course.num_labs, 3)
        self.assertEqual(da_course.instructor, "not_set@uwm.edu")

        # parameter errors
        # missing number of lab sections
        with self.assertRaises(TypeError):
            self.ad1.create_course("CS101-401")
        # missing course_id/wrong type
        with self.assertRaises(TypeError):
            self.ad1.create_course(3)
        # course_id too long and not right format
        with self.assertRaises(Exception):
            self.ad1.create_course("totally_a_good_course_id", 2)
        # course_id missing CS at beginning
        with self.assertRaises(Exception):
            self.ad1.create_course("123456789", 2)
        # course_id does not start with uppercase CS
        with self.assertRaises(Exception):
            self.ad1.create_course("cs361-401", 2)
        # course_id doesn't have only numbers for course number
        with self.assertRaises(Exception):
            self.ad1.create_course("CS3F4-321", 2)
        # course_id doesn't have a hyphen to separate course number and section number
        with self.assertRaises(Exception):
            self.ad1.create_course("CS3611234", 2)
        # course_id doesn't have only numbers for section number
        with self.assertRaises(Exception):
            self.ad1.create_course("CS361-1F3", 2)
        # number of sections too big
        with self.assertRaises(Exception):
            self.ad1.create_course("CS361-401", 99)
        # number of sections is less than 0
        with self.assertRaises(Exception):
            self.ad1.create_course("CS361-401", -1)

    # Create Account Tests
    # created by Jeff
    def test_create_instructor(self):
        # Create Instructor Tests
        # create unused instructor account
        self.assertTrue(self.ad1.create_account("DustyBottoms@uwm.edu", "better_password", "instructor"))
        # get account that was just setup
        test_model_ins = models.ModelPerson.objects.get(email="DustyBottoms@uwm.edu")
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

    def test_create_TA(self):
        # Create TA Tests
        # create unused ta account
        self.assertTrue(self.ad1.create_account("FredClaus@uwm.edu", "santa_bro", "ta"))
        # get account
        test_model_ta = models.ModelPerson.objects.get(email="FredClaus@uwm.edu")
        # test email
        self.assertEqual(test_model_ta.email, "FredClaus@uwm.edu")
        # test password
        self.assertEqual(test_model_ta.password, "santa_bro")
        # default name test
        self.assertEqual(test_model_ta.name, "DEFAULT")
        # default phone test
        self.assertEqual(test_model_ta.phone, -1)
        # login false test
        self.assertFalse(test_model_ta.isLoggedOn)

    # Invalid account type tests
    def test_create_invalid_account_supervisor(self):
        # create supervisor test
        self.assertFalse(self.ad1.create_account("superdude@uwm.edu", "super1", "supervisor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="superdude@uwm.edu")

    def test_create_invalid_account_administrator(self):
        # create admin test
        self.assertFalse(self.ad1.create_account("adminotaur@uwm.edu", "labyrinth", "administrator"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="adminotaur@uwm.edu")

    def test_create_invalid_account_other(self):
        # create whatever test
        self.assertFalse(self.ad1.create_account("farfelkugel@uwm.edu", "not_today", "horse"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="farfelkugel@uwm.edu")

    # Invalid parameter tests
    def test_create_invalid_parameter_no_email(self):
        # no email
        with self.assertRaises(TypeError):
            self.ad1.create_account("password", "instructor")

    def test_create_invalid_parameter_no_password(self):
        # no password
        with self.assertRaises(TypeError):
            self.ad1.create_account("no_password@uwm.edu", "instructor")

    def test_create_invalid_parameter_no_account_type(self):
        # no account type
        with self.assertRaises(TypeError):
            self.ad1.create_account("some_doof@uwm.edu", "password3")

    def test_create_invalid_parameter_non_uwm_email(self):
        # non uwm email
        self.assertFalse(self.ad1.create_account("bobross@bobross.com", "happy_trees", "instructor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="bobross@bobross.com")

    def test_create_invalid_parameter_weird_email(self):
        # weird email, props to Grant for this test
        self.assertFalse(self.ad1.create_account("bobross@uwm.edu@uwm.edu", "lotta_bob", "instructor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="bobross@uwm.edu@uwm.edu")

    def test_create_invalid_parameter_not_an_email_addy(self):
        # not really an email addy
        self.assertFalse(self.ad1.create_account("TRUST_ME_IM_EMAIL", "seriously_real_address", "ta"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="TRUST_ME_IM_EMAIL")

    def test_create_invalid_parameter_wrong_arg_types(self):
        # int args
        self.assertFalse(self.ad1.create_account(7, 8, 9))
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email=7)

    def test_create_invalid_parameter_taken_email(self):
        # email taken
        self.assertFalse(self.ad1.create_account("FredClaus@uwm.edu", "santa_bro", "ta"))

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
        # Jeff's tests

        # Admin/Sup only tests
        self.ad1 = Administrator("admin@uwm.edu", "password")
        self.sp1 = Supervisor("super@uwm.edu", "password")
        # access as admin
        access_info = self.ad1.access_info()
        # admin info
        self.assertEqual(access_info[0], "Administrator: DEFAULT | admin@uwm.edu | -1")
        self.assertEqual(access_info[1], "")
        # sup info
        self.assertEqual(access_info[2], "Supervisor: DEFAULT | super@uwm.edu | -1")
        self.assertEqual(access_info[3], "")
        # access as sup
        # is it ok to do this here? this is the only place where we test access info
        access_info = self.sp1.access_info()
        # admin info
        self.assertEqual(access_info[0], "Administrator: DEFAULT | admin@uwm.edu | -1")
        self.assertEqual(access_info[1], "")
        # sup info
        self.assertEqual(access_info[2], "Supervisor: DEFAULT | super@uwm.edu | -1")
        self.assertEqual(access_info[3], "")

        # Add instructor, no course assignments
        self.inst1 = Instructor("inst1@uwm.edu", "password")
        # access as admin
        access_info = self.ad1.access_info()
        self.assertEqual(access_info[4], "Instructor: DEFAULT | inst1@uwm.edu | -1")
        self.assertEqual(access_info[5], "")

        # Add TA, no course assignments
        self.ta1 = TA("ta1@uwm.edu", "password")
        # access as admin
        access_info = self.ad1.access_info()
        self.assertEqual(access_info[6], "TA: DEFAULT | ta1@uwm.edu | -1")
        self.assertEqual(access_info[7], "")

        # Instructor with a course
        self.course1 = Course("CS101", 0)
        self.course1.instructor = "inst1@uwm.edu"
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_course1.instructor = "inst1@uwm.edu"
        mod_course1.save()
        # access as admin
        access_info = self.ad1.access_info()
        self.assertEqual(access_info[5], "Course: CS101")

        # TA with a course
        mod_ta_course1 = models.ModelTACourse()
        mod_ta_course1.course = mod_course1
        mod_ta1 = models.ModelTA.objects.get(email="ta1@uwm.edu")
        mod_ta_course1.TA = mod_ta1
        mod_ta_course1.save()
        access_info = self.ad1.access_info()
        self.assertEqual(access_info[8], "Course: CS101")

        # commenting out old tests, writing my own - Jeff
        # creating stuff in the system
        # self.user = ("email@uwm.edu", "pass")
        # self.system_stuff = ([self.ad1, self.ad2, self.user],
                            # ["ad1@uwm.edu", "ad2@uwm.edu", "email@uwm.edu"],
                            # ["ad1pass", "ad2pass", "pass"])
        # self.assertEqual(self.ad1.access_info(), self.system_stuff)

    # models.ModelPerson.objects.all().delete()
