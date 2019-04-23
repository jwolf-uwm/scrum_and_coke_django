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
            print(f"{course_id} is too short to be of the right form (CS###-###)")
            return False
        if course_id[0:2] != "CS":
            print(f"{course_id} is not a CS course (CS###-###)")
            return False
        if not course_id[2:5].isdigit():
            print("The course number contains an invalid digit (CS###-###)")
            return False
        if course_id[5] != "-":
            print("The course and section number should be separated by a hyphen (CS###-###)")
            return False
        if not course_id[6:].isdigit():
            print("The section number contains an invalid digit (CS###-###)")
            return False
        if num_labs < 0 or num_labs > 5:
            print("The number of lab sections should be positive and not exceed 5")
            return False
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
            try:
                find_email = models.ModelPerson.objects.get(email=email)
            except models.ModelPerson.DoesNotExist:
                find_email = "none"

            if find_email == "none":
                return False

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

        elif field == "phone":
            parse_phone = content.split(".")
            if len(parse_phone) != 3:
                print("Bad length")
                return False
            if not parse_phone[0].isdigit() or not parse_phone[1].isdigit() or not parse_phone[2].isdigit():
                print("Not digits")
                return False
            if len(parse_phone[0]) != 3 or len(parse_phone[1]) != 3 or len(parse_phone[2]) != 4:
                print("Substrings bad length")
                return False
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
        # returns a string of all users/courses in the system
        # with appropriate linebreaks for display

        string_list = "Administrator:\n"

        admins = models.ModelPerson.objects.filter(type="administrator")
        for admin in admins:
            string_list = string_list + admin.name + " | " + admin.email + " | " + \
                          str(admin.phone) + "\n"
            string_list = string_list + "\n"

        string_list = string_list + "Supervisor:\n"

        supers = models.ModelPerson.objects.filter(type="supervisor")
        for supervi in supers:
            string_list = string_list + supervi.name + " | " + supervi.email + " | " + \
                          str(supervi.phone) + "\n"
            string_list = string_list + "\n"

        string_list = string_list + "Instructors:\n"

        instructs = models.ModelPerson.objects.filter(type="instructor")
        for instruct in instructs:
            string_list = string_list + instruct.name + " | " + instruct.email + " | " + \
                          str(instruct.phone) + "\n"

            for courses in models.ModelCourse.objects.all():
                if courses.instructor == instruct.email:
                    string_list = string_list + "Course: " + courses.course_id + "\n"

        string_list = string_list + "\n"

        string_list = string_list + "TAs:\n"

        tee_ayys = models.ModelPerson.objects.filter(type="ta")
        for tee_ayy in tee_ayys:
            string_list = string_list + tee_ayy.name + " | " + tee_ayy.email + " | " + str(tee_ayy.phone) + \
                          "\n"

            for ta_courses in models.ModelTACourse.objects.all():
                if ta_courses.TA.email == tee_ayy.email:
                    string_list = string_list + "Course: " + ta_courses.course.course_id + "\n"

        string_list = string_list + "\n"

        string_list = string_list + "Courses:\n"
        courses = models.ModelCourse.objects.all()
        for course in courses:
            string_list = string_list + course.course_id + "\n"
        return string_list
