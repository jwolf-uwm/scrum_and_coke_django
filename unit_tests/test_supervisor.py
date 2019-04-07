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
        self.ad1 = Administrator("ad1@uwm.edu", "ad1pass", "administrator")
        self.sup1 = Supervisor("sup1@uwm.edu", "sup1pass", "supervisor")

    def test_assign_instructor_course(self):
        # fake instructors
        self.ins1 = Instructor("ins1@uwm.edu", "blah", "instructor")
        self.ins2 = Instructor("ins2@uwm.edu", "inspass", "instructor")
        # fake course
        self.course1 = Course("CS101", 2)
        self.course2 = Course("CS202", 0)
        # instructor 1 is assigned CS101
        self.assertTrue(self.sup1.assign_instructor(self.ins1, self.course1))
        # self.assertEqual(self.ins1.courses[0], self.course1)
        self.assertEqual(self.course1.instructor.email, "ins1@uwm.edu")

        # assign instructor 1 another course
        self.assertTrue(self.sup1.assign_instructor(self.ins1, self.course2))
        # self.assertEqual(self.ins1.courses[1], self.course2)
        self.assertEqual(self.course2.instructor.email, "ins1@uwm.edu")

        # instructor 2 is assigned CS101
        self.assertTrue(self.sup1.assign_instructor(self.ins2, self.course1))
        # self.assertEqual(self.ins2.courses[0], self.course1)
        self.assertEqual(self.course1.instructor.email, "ins2@uwm.edu")
        # self.assertNotEqual(self.ins1.courses[0], self.course1)

        self.ta1 = TA("ta1@uwm.edu", "beh", "TA")
        with self.assertRaises(TypeError):
            self.sup1.assign_instructor(self.ta1, self.course1)

        self.admin1 = Administrator("admin@uwm.edu", "admin1", "administrator")
        with self.assertRaises(TypeError):
            self.sup1.assign_instructor(self.admin1, self.course1)

        with self.assertRaises(TypeError):
            self.sup1.assign_instructor(self.sup1, self.course1)

        with self.assertRaises(AttributeError):
            self.sup1.assign_instructor(self.ins1, "CS301-111")

        with self.assertRaises(AttributeError):
            self.sup1.assign_instructor("ins1@uwm.edu", self.course1)

        self.sup1.create_course("CS337-401", 3)
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
        self.ta1 = TA("ta1@uwm.edu", "blah", "ta")
        self.ta2 = TA("ta2@uwm.edu", "inspass", "ta")
        self.ta3 = TA("ta3@uwm.edu", "pass3", "ta")
        # fake course
        self.course1 = Course("CS101-301", 2)
        self.course2 = Course("CS202-201", 0)
        # instructor 1 is assigned CS101
        self.assertTrue(self.sup1.assign_ta_course(self.ta1, self.course1))
        self.assertEqual(self.course1.tee_ays[0], "ta1@uwm.edu")
        db_ta_course = models.ModelTACourse.objects.get(course=models.ModelCourse.objects.get(course_id="CS101-301"), TA=models.ModelPerson.objects.get(email="ta1@uwm.edu"))
        self.assertEqual(db_ta_course.TA, models.ModelPerson.objects.get(email="ta1@uwm.edu"))
        self.assertEqual(db_ta_course.course, models.ModelCourse.objects.get(course_id="CS101-301"))

        # assign TA 1 another course
        self.assertTrue(self.sup1.assign_ta_course(self.ta1, self.course2))
        self.assertEqual(self.course1.tee_ays[0], "ta1@uwm.edu")
        db_ta_course = models.ModelTACourse.objects.get(course=models.ModelCourse.objects.get(course_id="CS202-201"),
                                                        TA=models.ModelPerson.objects.get(email="ta1@uwm.edu"))
        self.assertEqual(db_ta_course.TA, models.ModelPerson.objects.get(email="ta1@uwm.edu"))
        self.assertEqual(db_ta_course.course, models.ModelCourse.objects.get(course_id="CS202-201"))

        # TA 2 is assigned CS101
        self.assertTrue(self.sup1.assign_ta_course(self.ta2, self.course1))
        self.assertEqual(self.course1.tee_ays[0], "ta1@uwm.edu")
        db_ta_course = models.ModelTACourse.objects.get(course=models.ModelCourse.objects.get(course_id="CS101-301"),
                                                        TA=models.ModelPerson.objects.get(email="ta2@uwm.edu"))
        self.assertEqual(db_ta_course.TA, models.ModelPerson.objects.get(email="ta2@uwm.edu"))
        self.assertEqual(db_ta_course.course, models.ModelCourse.objects.get(course_id="CS101-301"))

        # Try to assign a third TA to CS101
        self.assertTrue(self.sup1.assign_ta_course(self.ta3, self.course1))
        self.assertEqual(self.course1.tee_ays[0], "ta1@uwm.edu")
        db_ta_course = models.ModelTACourse.objects.get(course=models.ModelCourse.objects.get(course_id="CS101-301"),
                                                        TA=models.ModelPerson.objects.get(email="ta3@uwm.edu"))
        self.assertEqual(db_ta_course.TA, models.ModelPerson.objects.get(email="ta3@uwm.edu"))
        self.assertEqual(db_ta_course.course, models.ModelCourse.objects.get(course_id="CS101-301"))

        self.admin1 = Administrator("admin@uwm.edu", "admin1", "administrator")
        with self.assertRaises(TypeError):
            self.sup1.assign_ta_course(self.admin1, self.course1)

        with self.assertRaises(TypeError):
            self.sup1.assign_ta_course(self.sup1, self.course1)

        self.ins1 = Instructor("ins@uwm.edu", "ins11111", "instructor")
        with self.assertRaises(TypeError):
            self.sup1.assign_ta_course(self.ins1, self.course1)

        with self.assertRaises(AttributeError):
            self.sup1.assign_ta_course(self.ta1, "CS301-111")

        with self.assertRaises(AttributeError):
            self.sup1.assign_ta_course("ta1@uwm.edu", self.course1)

    def test_assign_ta_lab(self):
        # TA 1 is assigned CS101 - 801
        self.sup1.assign_ta_lab(self.ta1, "CS101", 801)
        self.assertEqual(self.ta1_sections[0], 801)

        # TA 2 is assigned CS101 - 802
        self.sup1.assign_ta_lab(self.ta2, 802)
        self.assertEqual(self.ta2_sections[0], "CS101")

        # Try to assign TA 1 another lab section
        self.assertRaises(self.sup1.assign_ta_lab(self.ta1, self.course2[0]), OverflowError)

        self.assertRaises(self.sup1.assign_ta_lab(self.ins1, self.course1[0]), TypeError)

    # Create Account Tests Start
    # created by Jeff
    def test_create_account_instructor(self):
        # Create Instructor Tests
        # create unused instructor account
        self.assertTrue(self.sup1.create_account("DustyBottoms@uwm.edu", "better_password", "instructor"))
        # get account that was just setup
        test_model_ins = models.ModelPerson.objects.get(email="DustyBottoms@uwm.edu")
        # make sure email is equal
        self.assertEqual(test_model_ins.email, "DustyBottoms@uwm.edu")
        # make sure password is equal
        self.assertEqual(test_model_ins.password, "better_password")
        # default name test
        self.assertEqual(test_model_ins.name, "DEFAULT")
        # default phone test
        self.assertEqual(test_model_ins.phone, "000.000.0000")
        # login false test
        self.assertFalse(test_model_ins.isLoggedOn)

    def test_create_account_TA(self):
        # Create TA Tests
        # create unused ta account
        self.assertTrue(self.sup1.create_account("FredClaus@uwm.edu", "santa_bro", "ta"))
        # get account
        test_model_ta = models.ModelPerson.objects.get(email="FredClaus@uwm.edu")
        # test email
        self.assertEqual(test_model_ta.email, "FredClaus@uwm.edu")
        # test password
        self.assertEqual(test_model_ta.password, "santa_bro")
        # default name test
        self.assertEqual(test_model_ta.name, "DEFAULT")
        # default phone test
        self.assertEqual(test_model_ta.phone, "000.000.0000")
        # login false test
        self.assertFalse(test_model_ta.isLoggedOn)

    # Invalid account type tests
    def test_create_account_supervisor(self):
        # create supervisor test
        self.assertFalse(self.sup1.create_account("superdude@uwm.edu", "super1", "supervisor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="superdude@uwm.edu")

    def test_create_account_administrator(self):
        # create admin test
        self.assertFalse(self.sup1.create_account("adminotaur@uwm.edu", "labyrinth", "administrator"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="adminotaur@uwm.edu")

    def test_create_account_other(self):
        # create whatever test
        self.assertFalse(self.sup1.create_account("farfelkugel@uwm.edu", "not_today", "horse"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="farfelkugel@uwm.edu")

    # Invalid parameter tests
    def test_create_account_invalid_parameter_no_email(self):
        # no email
        with self.assertRaises(TypeError):
            self.sup1.create_account("password", "instructor")

    def test_create_account_invalid_parameter_no_password(self):
        # no password
        with self.assertRaises(TypeError):
            self.sup1.create_account("no_password@uwm.edu", "instructor")

    def test_create_account_invalid_parameter_no_account_type(self):
        # no account type
        with self.assertRaises(TypeError):
            self.sup1.create_account("some_doof@uwm.edu", "password3")

    def test_create_account_invalid_parameter_non_uwm_email(self):
        # non uwm email
        self.assertFalse(self.sup1.create_account("bobross@bobross.com", "happy_trees", "instructor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="bobross@bobross.com")

    def test_create_account_invalid_parameter_weird_email(self):
        # weird email, props to Grant for this test
        self.assertFalse(self.sup1.create_account("bobross@uwm.edu@uwm.edu", "lotta_bob", "instructor"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="bobross@uwm.edu@uwm.edu")

    def test_create_account_invalid_parameter_not_an_email_addy(self):
        # not really an email addy
        self.assertFalse(self.sup1.create_account("TRUST_ME_IM_EMAIL", "seriously_real_address", "ta"))
        # not in db
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email="TRUST_ME_IM_EMAIL")

    def test_create_account_invalid_parameter_wrong_arg_types(self):
        # int args
        self.assertFalse(self.sup1.create_account(7, 8, 9))
        with self.assertRaises(models.ModelPerson.DoesNotExist):
            models.ModelPerson.objects.get(email=7)

    def test_create_account_invalid_parameter_taken_email(self):
        # email taken
        self.sup1.create_account("FredClaus@uwm.edu", "santa_bro", "ta")
        self.assertFalse(self.sup1.create_account("FredClaus@uwm.edu", "santa_bro", "ta"))

    # Create Account Tests End

    # Access Info Tests Start
    # Jeff's tests
    def test_access_info_admin_title(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[0], "Administrator:")

    def test_access_info_admin_(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[1], "DEFAULT | ad1@uwm.edu | 000.000.0000")

    def test_access_info_blank_one(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[2], "")

    def test_access_info_sup_title(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[3], "Supervisor:")

    def test_access_info_sup(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[4], "DEFAULT | sup1@uwm.edu | 000.000.0000")

    def test_access_info_blank_two(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[5], "")

    def test_access_info_inst_title(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[6], "Instructors:")

    def test_access_info_blank_three(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[7], "")

    def test_access_info_ta_title(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[8], "TAs:")

    def test_access_info_blank_four(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[9], "")

    def test_access_info_course_title(self):
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[10], "Courses:")

    def test_access_info_inst_no_course(self):
        # Add instructor, no course assignments
        self.inst1 = Instructor("inst1@uwm.edu", "password", "instructor")
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")

    def test_access_info_ta_no_course(self):
        # Add TA, no course assignments
        self.ta1 = TA("ta1@uwm.edu", "password", "ta")
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[9], "DEFAULT | ta1@uwm.edu | 000.000.0000")

    def test_access_info_inst_one_course(self):
        # Instructor with a course
        self.inst1 = Instructor("inst1@uwm.edu", "password", "instructor")
        self.course1 = Course("CS101", 0)
        self.course1.instructor = "inst1@uwm.edu"
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_course1.instructor = "inst1@uwm.edu"
        mod_course1.save()
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[8], "Course: CS101")

    def test_access_info_ta_one_course(self):
        # TA with a course
        self.ta1 = TA("ta1@uwm.edu", "password", "ta")
        mod_ta_course1 = models.ModelTACourse()
        self.course1 = Course("CS101", 0)
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_ta_course1.course = mod_course1
        mod_ta1 = models.ModelPerson.objects.get(email="ta1@uwm.edu")
        mod_ta_course1.TA = mod_ta1
        mod_ta_course1.save()
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[10], "Course: CS101")

    def test_access_info_course(self):
        # just a course
        self.course1 = Course("CS101", 0)
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[11], "CS101")

    def test_access_info_all_the_things(self):
        # ALL THE THINGS
        self.inst1 = Instructor("inst1@uwm.edu", "password", "instructor")
        self.inst2 = Instructor("inst2@uwm.edu", "password", "instructor")
        self.ta1 = TA("ta1@uwm.edu", "password", "ta")
        self.ta2 = TA("ta2@uwm.edu", "password", "ta")
        self.course1 = Course("CS101", 0)
        self.course2 = Course("CS102", 0)
        self.course1.instructor = "inst1@uwm.edu"
        mod_course1 = models.ModelCourse.objects.get(course_id="CS101")
        mod_course1.instructor = "inst1@uwm.edu"
        mod_course1.save()
        self.course2.instructor = "inst2@uwm.edu"
        mod_course2 = models.ModelCourse.objects.get(course_id="CS102")
        mod_course2.instructor = "inst2@uwm.edu"
        mod_course2.save()
        mod_ta_course1 = models.ModelTACourse()
        mod_ta_course1.course = mod_course1
        mod_ta1 = models.ModelPerson.objects.get(email="ta1@uwm.edu")
        mod_ta_course1.TA = mod_ta1
        mod_ta_course1.save()
        mod_ta_course2 = models.ModelTACourse()
        mod_ta_course2.course = mod_course2
        mod_ta2 = models.ModelPerson.objects.get(email="ta2@uwm.edu")
        mod_ta_course2.TA = mod_ta2
        mod_ta_course2.save()
        access_info = self.sup1.access_info()
        parse_info = access_info.split("\n")
        self.assertEqual(parse_info[0], "Administrator:")
        self.assertEqual(parse_info[1], "DEFAULT | ad1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[2], "")
        self.assertEqual(parse_info[3], "Supervisor:")
        self.assertEqual(parse_info[4], "DEFAULT | sup1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[5], "")
        self.assertEqual(parse_info[6], "Instructors:")
        self.assertEqual(parse_info[7], "DEFAULT | inst1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[8], "Course: CS101")
        self.assertEqual(parse_info[9], "DEFAULT | inst2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[10], "Course: CS102")
        self.assertEqual(parse_info[11], "")
        self.assertEqual(parse_info[12], "TAs:")
        self.assertEqual(parse_info[13], "DEFAULT | ta1@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[14], "Course: CS101")
        self.assertEqual(parse_info[15], "DEFAULT | ta2@uwm.edu | 000.000.0000")
        self.assertEqual(parse_info[16], "Course: CS102")
        self.assertEqual(parse_info[17], "")
        self.assertEqual(parse_info[18], "Courses:")
        self.assertEqual(parse_info[19], "CS101")
        self.assertEqual(parse_info[20], "CS102")

    # Access Info Tests End
