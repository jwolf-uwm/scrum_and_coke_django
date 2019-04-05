# created by Dillan

from classes.Person import Person
from ta_assign import models


class TA(Person):

    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)

    def view_ta_assignments(self):
        assignment_list = []
        ta_assignments = models.ModelTACourse.objects.all()
        for i in ta_assignments:
            assignment_list.append("Course: " + ta_assignments[i].course + "TA: " + ta_assignments[i].TA + " | ")
        return assignment_list

    def read_public_contact(self, class_list):
        return

    def edit_contact_info(self, field, content):
        return
