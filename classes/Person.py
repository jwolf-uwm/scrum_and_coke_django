# created by Grant
from ta_assign import models


class Person:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.phone_number = -1
        self.name = "DEFAULT"
        self.isLoggedIn = False

        some_guy = models.ModelPerson()
        some_guy.email = self.email
        some_guy.password = self.password
        some_guy.name = self.name
        some_guy.phone = self.phone_number
        some_guy.isLoggedOn = self.isLoggedIn
        some_guy.save()

        print("BIG BUTTS")

        test_query = models.ModelPerson.objects.all()
        test_list = []

        for i in test_query:
            test_list.append(i)

        print(test_list[0].email)

    def change_password(self, old, new):
        return

    def change_email(self, address):
        return

    def change_name(self, name):
        return

    def change_phone(self, phone):
        return

    def get_contact_info(self):
        return

    def login(self, email, password):

        if self.email != email or self.password != password:
            return "Invalid login info."
        if self.isLoggedIn is True:
            return "User already logged in"
        self.isLoggedIn = True
        return "Login successful."

    def logout(self):

        if self.isLoggedIn is False:
            return False
        self.isLoggedIn = False
        return True
