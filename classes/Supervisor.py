# created by Evan

from classes.Administrator import Administrator
from classes.Person import Person
from classes.Course import Course
from classes.Instructor import Instructor
from ta_assign import models


class Supervisor(Administrator):
    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)

    def assign_instructor(self, instructor, course):
        """
        assigns the given instructor's course to the course parameter
        """
        if instructor.type != "instructor":
            raise TypeError("invalid type")
        try:
            find_course = models.ModelCourse.objects.get(course_id=course.course_id)
        except models.ModelCourse.DoesNotExist:
            find_course = "none"

        try:
            find_instructor = models.ModelPerson.objects.get(email=instructor.email)
        except models.ModelPerson.DoesNotExist:
            find_instructor = "none"

        if find_course != "none" and find_instructor != "none":
            find_course.instructor = instructor.email
            #if course.instructor != "not_set@uwm.edu":
            #    course.instructor.courses.remove(course)
            course.instructor = instructor
            # instructor.courses.append(course)
            return True
        else:
            return False

    def assign_ta_course(self, ta, course):
        """
        assigns the given TA's course to the course parameter
        """
        if ta.type != "ta":
            raise TypeError("invalid type")
        try:
            find_course = models.ModelCourse.objects.get(course_id=course.course_id)
        except models.ModelCourse.DoesNotExist:
            find_course = "none"

        try:
            find_ta = models.ModelPerson.objects.get(email=ta.email)
        except models.ModelCourse.DoesNotExist:
            find_ta = "none"

        if find_course != "none" and find_ta != "none":
            ta_course = models.ModelTACourse()
            ta_course.TA = find_ta
            ta_course.course = find_course
            course.tee_ays.append(ta.email)
            ta_course.save()
            return True
        else:
            return False
        return False

    def assign_ta_lab(self, email, course_id, lab_section):
        """
        assigns the given TA's lab
        """
        return
