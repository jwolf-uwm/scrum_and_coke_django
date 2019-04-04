# created by Grant
from ta_assign import models


class Person:
    def __init__(self, email, password, account_type):
        self.email = email
        self.password = password
        self.phone_number = -1
        self.name = "DEFAULT"
        self.type = account_type
        self.isLoggedOn = False

        try:
            find_email = models.ModelPerson.objects.get(email=email)
        except models.ModelPerson.DoesNotExist:
            find_email = "none"

        if find_email == "none":
            some_guy = models.ModelPerson()
            some_guy.email = self.email
            some_guy.password = self.password
            some_guy.name = self.name
            some_guy.phone = self.phone_number
            some_guy.type = self.type
            some_guy.isLoggedOn = self.isLoggedOn
            some_guy.save()

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

    @staticmethod
    def login(email, password):

        people = models.ModelPerson.objects.all()

        temp = None

        for i in people:
            if i.email == email:
                temp = i

        if temp is None:
            return "Invalid login info"
        elif temp.email != email or temp.password != password:
            return "Invalid login info"
        if temp.isLoggedOn is True:
            return "User already logged in"
        temp.isLoggedOn = True
        temp.save()
        return "Login successful"

    def logout(self):

        if self.isLoggedOn is False:
            return False
        self.isLoggedOn = False
        return True
