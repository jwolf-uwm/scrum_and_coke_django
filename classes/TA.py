# created by Dillan

from classes.Person import Person
from ta_assign import models


class TA(Person):

    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)

    def view_ta_assignments(self):
        assignment_list = []
        ta_courses = models.ModelTACourse.objects.all()
        for i in ta_courses:
            assignment_list.append("Course: " + ta_courses[i].course.course_id + "TA: " + ta_courses[i].TA.email + " | ")
        return assignment_list

    def read_public_contact(self, class_list):
        return

    def edit_contact_info(self, field, content):
        return
