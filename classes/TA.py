# created by Dillan

from classes.Person import Person


class TA(Person):

    def __init__(self, email, password):
        super().__init__(email, password)

    def view_ta_assignments(self, course_catalog):
        return

    def read_public_contact(self, class_list):
        return

    def edit_contact_info(self, field, content):
        return
