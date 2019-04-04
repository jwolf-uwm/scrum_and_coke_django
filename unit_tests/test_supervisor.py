# created by Evan

from django.test import TestCase
from classes.Supervisor import Supervisor
from ta_assign import models

class TestSupervisor(TestCase):

    def setUp(self):
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
        self.sup = Supervisor("sup@uwm.edu", "sup_pass", "supervisor")

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

    # Create Account Tests
    # created by Jeff
    def test_create_account_instructor(self):
        # Create Instructor Tests
        # create unused instructor account
        self.assertTrue(self.sup.create_account("DustyBottoms@uwm.edu", "better_password", "instructor"))
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

    def test_create_account_TA(self):
        # Create TA Tests
        # create unused ta account
        self.assertTrue(self.sup.create_account("FredClaus@uwm.edu", "santa_bro", "ta"))
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
    def test_create_account_supervisor(self):
        # create supervisor test
        self.assertFalse(self.sup.create_account("superdude@uwm.edu", "super1", "supervisor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="superdude@uwm.edu")

    def test_create_account_administrator(self):
        # create admin test
        self.assertFalse(self.sup.create_account("adminotaur@uwm.edu", "labyrinth", "administrator"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="adminotaur@uwm.edu")

    def test_create_account_other(self):
        # create whatever test
        self.assertFalse(self.sup.create_account("farfelkugel@uwm.edu", "not_today", "horse"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="farfelkugel@uwm.edu")

    # Invalid parameter tests
    def test_create_account_invalid_parameter_no_email(self):
        # no email
        with self.assertRaises(TypeError):
            self.sup.create_account("password", "instructor")

    def test_create_account_invalid_parameter_no_password(self):
        # no password
        with self.assertRaises(TypeError):
            self.sup.create_account("no_password@uwm.edu", "instructor")

    def test_create_account_invalid_parameter_no_account_type(self):
        # no account type
        with self.assertRaises(TypeError):
            self.sup.create_account("some_doof@uwm.edu", "password3")

    def test_create_account_invalid_parameter_non_uwm_email(self):
        # non uwm email
        self.assertFalse(self.sup.create_account("bobross@bobross.com", "happy_trees", "instructor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="bobross@bobross.com")

    def test_create_account_invalid_parameter_weird_email(self):
        # weird email, props to Grant for this test
        self.assertFalse(self.sup.create_account("bobross@uwm.edu@uwm.edu", "lotta_bob", "instructor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="bobross@uwm.edu@uwm.edu")

    def test_create_account_invalid_parameter_not_an_email_addy(self):
        # not really an email addy
        self.assertFalse(self.sup.create_account("TRUST_ME_IM_EMAIL", "seriously_real_address", "ta"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="TRUST_ME_IM_EMAIL")

    def test_create_account_invalid_parameter_wrong_arg_types(self):
        # int args
        self.assertFalse(self.sup.create_account(7, 8, 9))
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email=7)

    def test_create_account_invalid_parameter_taken_email(self):
        # email taken
        self.sup.create_account("FredClaus@uwm.edu", "santa_bro", "ta")
        self.assertFalse(self.sup.create_account("FredClaus@uwm.edu", "santa_bro", "ta"))