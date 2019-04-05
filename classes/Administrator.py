# created by Matt

from classes.Person import Person
from classes.Instructor import Instructor
from classes.TA import TA
from classes.Course import Course
# from classes.Database import Database
from ta_assign import models


class Administrator(Person):
    """
    an instance represents an administrator within the schools
    system
    must have username
    must have password
    must be able to create courses
    must be able to create accounts
    must be able to edit accounts
    must be able to delete account
    must be able to send notification
    must be able to access information
    """
    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)

    def create_course(self, course_id, num_labs):
        if len(course_id) != 9:
            raise Exception("{} is too short to be of the right form (CS###-###)".format(course_id))
        if course_id[0:2] != "CS":
            raise Exception("{} is not a CS course (CS###-###)".format(course_id))
        if not course_id[2:5].isdigit():
            raise Exception("The course number contains an invalid digit (CS###-###)")
        if course_id[5] != "-":
            raise Exception("The course and section number should be separated by a hyphen (CS###-###)")
        if not course_id[6:].isdigit():
            raise Exception("The section number contains an invalid digit (CS###-###)")
        if num_labs < 0 or num_labs > 5:
            raise Exception("The number of lab sections should be positive and not exceed 5")
        try:
            find_course = models.ModelCourse.objects.get(course_id=course_id)
        except models.ModelCourse.DoesNotExist:
            find_course = "none"

        if find_course != "none":
            return False

        new_course = Course(course_id, num_labs)
        return True

    def create_account(self, email, password, account_type):
        # Jeff's method
        # Usage: (string: email, string: password, string: account_type)
        # returns True if account successfully created in DB
        # returns False if account was unable to be created
        # throws exceptions if you do it wrong

        if account_type != "instructor" and account_type != "ta":
            return False

        try:
            find_email = models.ModelPerson.objects.get(email=email)
        except models.ModelPerson.DoesNotExist:
            find_email = "none"

        if find_email != "none":
            return False

        parse_at = email.split("@")

        try:
            if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                return False
        except IndexError:
            return False

        if account_type == "instructor":
            new_instructor = Instructor(email, password, "instructor")
            return True

        elif account_type == "ta":
            new_ta = TA(email, password, "ta")
            return True

    def edit_account(self, email, field, content):
        try:
            models.ModelPerson.objects.get(email=email)
        except models.ModelPerson.DoesNotExist:
            return False

        if field == "email":
            parse_at = content.split("@")
            try:
                if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                    return False
            except ValueError:
                return False
            models.ModelPerson.objects.filter(email=email).update(email=content)
            return True

        elif field == "password":
            models.ModelPerson.objects.filter(email=email).update(password=content)
            return True

        elif field == "phone_number":
            if not isinstance(content, int):
                print("phone number contains illegal characters")
                return False
            elif int(content / 1000000000) >= 10 or int(content / 1000000000) <= 0:
                print("phone number is the wrong length")
                return False
            else:
                models.ModelPerson.objects.filter(email=email).update(phone=content)
                return True

        elif field == "name":
            models.ModelPerson.objects.filter(email=email).update(name=content)
            return True
        else:
            print("The entered field is incorrect")
            return False

    def delete_account(self, email):
        return

    def send_notification(self, notification):
        return

    def access_info(self):
        # Jeff's method
        # Usage: access_info()
        # returns a list of strings of all users in the database
        # each string is as follows:
        #   "ACCOUNT_TYPE: name | email address | phone"
        # if user is instructor following strings are:
        #   "Classes assigned: class1, class2, class3"
        #   "TAs assigned : ta1, ta2, ta3"
        # if user is ta, following strings are:
        #   "Classes assigned: class1, class2, class3"
        #   NOT IMPLEMENTED: "Labs assigned: lab1, lab2, lab3"

        string_list = []

        admins = models.ModelPerson.objects.filter(type="administrator")
        for admin in admins:
            string_list.append("Administrator: " + admin.name + " | " + admin.email + " | " + str(admin.phone))
            string_list.append("")

        supers = models.ModelPerson.objects.filter(type="supervisor")
        for supervi in supers:
            string_list.append("Supervisor: " + supervi.name + " | " + supervi.email + " | " + str(supervi.phone))
            string_list.append("")

        instructs = models.ModelPerson.objects.filter(type="instructor")
        for instruct in instructs:
            string_list.append("Instructor: " + instruct.name + " | " + instruct.email + " | " + str(instruct.phone))

            for courses in models.ModelCourse.objects.all():
                if courses.instructor == instruct.email:
                    string_list.append("Course: " + courses.course_id)

            string_list.append("")

        tee_ayys = models.ModelPerson.objects.filter(type="ta")
        for tee_ayy in tee_ayys:
            string_list.append("TA: " + tee_ayy.name + " | " + tee_ayy.email + " | " + str(tee_ayy.phone))

            for ta_courses in models.ModelTACourse.objects.all():
                if ta_courses.TA.email == tee_ayy.email:
                    string_list.append("Course: " + ta_courses.course.course_id)

            string_list.append("")

        courses = models.ModelCourse.objects.all()
        for course in courses:
            string_list.append("Course: " + course.course_id)

            string_list.append("")
        return string_list
