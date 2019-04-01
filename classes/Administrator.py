# created by Matt

from classes.Person import Person
from classes.Instructor import Instructor
from classes.TA import TA
# from classes.Course import Course
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
    def __init__(self, email, password):
        super().__init__(email, password)

        some_guy = models.ModelAdministrator()
        some_guy.email = self.email
        some_guy.password = self.password
        some_guy.name = self.name
        some_guy.phone = self.phone_number
        some_guy.isLoggedOn = self.isLoggedIn
        some_guy.save()

    def create_course(self, course_id, num_labs):
        # new_course = Course(course_id, num_labs)
        # if Database.courses.contains(course_id):
        #    return "Course already exists"
        # Database.courses.append(course_id)
        # return new_course
        return

    def create_account(self, email, password, account_type):

        if account_type == "instructor":
            try:
                find_email = models.ModelInstructor.objects.get(email=email)
            except models.ModelInstructor.DoesNotExist:
                find_email = "none"

        elif account_type == "ta":
            try:
                find_email = models.ModelTA.objects.get(email=email)
            except models.ModelTA.DoesNotExist:
                find_email = "none"

        else:
            return False

        if find_email != "none":
            return False

        parse_at = email.split("@")

        if parse_at[1] != "uwm.edu":
            return False

        if account_type == "instructor":
            new_instructor = Instructor(email, password)
            return True

        elif account_type == "ta":
            new_ta = TA(email, password)
            return True

    def edit_account(self, email, field, content):
        return

    def delete_account(self, email):
        return

    def send_notification(self, notification):
        return

    def access_info(self):
        return
