# created by Dillan

from classes.Person import Person
from ta_assign import models


class TA(Person):

    def __init__(self, email, password):
        super().__init__(email, password)

        some_guy = models.ModelTA()
        some_guy.email = self.email
        some_guy.password = self.password
        some_guy.name = self.name
        some_guy.phone = self.phone_number
        some_guy.isLoggedOn = self.isLoggedIn
        some_guy.save()

    def view_ta_assignments(self, course_catalog):
        return

    def read_public_contact(self, class_list):
        return

    def edit_contact_info(self, field, content):
        return
