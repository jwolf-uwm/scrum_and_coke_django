# created by Dillan

from classes.Person import Person
from ta_assign import models


class TA(Person):

    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)
        some_instructor = models.ModelPerson()
        some_instructor.email = email
        some_instructor.password = password
        some_instructor.type = account_type

    def view_ta_assignments(self, course_catalog):
        return

    def read_public_contact(self, class_list):
        return

    def edit_contact_info(self, field, content):
        return
