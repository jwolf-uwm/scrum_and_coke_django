# created by Evan

from classes.Person import Person
from classes.Course import Course


class Supervisor(Person):
    def __init__(self, email, password):
        super().__init__(email, password)

    def assign_instructor(self, email, course_id, section_id):
        """
        assigns the given instructor's course to the course parameter
        """
        course_id.instructor = email
        return

    def assign_ta_course(self, email, course_id, course_section):
        """
        assigns the given TA's course to the course parameter
        """
        course_id.tee_ays.append(email)
        return

    def assign_ta_lab(self, email, course_id, lab_section):
        """
        assigns the given TA's lab
        """
        return

