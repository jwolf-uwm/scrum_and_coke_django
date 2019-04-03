# created by Evan

from classes.Administrator import Administrator
from classes.Person import Person
from classes.Course import Course
from ta_assign import models


class Supervisor(Administrator):
    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)

    def assign_instructor(self, email, course_id, section_id):
        """
        assigns the given instructor's course to the course parameter
        """
        try:
            find_course = models.ModelCourse.objects.get(course_id=course_id)
        except models.ModelCourse.DoesNotExist:
            find_course = "none"

        if find_course != "none":
            find_course.instructor = email
        else:
            print("No such course")
        return

    def assign_ta_course(self, email, course_id, course_section):
        """
        assigns the given TA's course to the course parameter
        """
        try:
            ta_course = models.ModelTACourseCourse.objects.get(course_id=course_id)
        except models.ModelCourse.DoesNotExist:
            ta_course = "none"

        if ta_course != "none":
            ta_course.TA
        else:
            print("No such course")
        course_id.tee_ays.append(email)
        return

    def assign_ta_lab(self, email, course_id, lab_section):
        """
        assigns the given TA's lab
        """
        return
