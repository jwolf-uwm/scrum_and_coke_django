# created by Grant
from ta_assign import models


class Person:
    def __init__(self, email, password, account_type):
        self.email = email
        self.password = password
        self.phone_number = "000.000.0000"
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

    def change_password(self, new):
        self.password = new
        return True

    def change_email(self, address):
        parse_at = address.split("@")

        try:
            if len(parse_at) != 2 or parse_at[1] != "uwm.edu":
                return False
        except ValueError:
            return False

        self.email = address
        return True

    def change_name(self, name):
        self.name = name
        return True

    def change_phone(self, phone):
        parse_phone = phone.split(".")
        if len(parse_phone) != 3:
            return False
        if not parse_phone[0].isdigit() or not parse_phone[1].isdigit() or not parse_phone[2].isdigit():
            return False
        if len(parse_phone[0]) != 3 or len(parse_phone[1]) != 3 or len(parse_phone[2]) != 4:
            return False

        self.phone_number = phone
        return True

    def get_contact_info(self):
        return

    @staticmethod
    def login(email, password):

        people = models.ModelPerson.objects.all()

        temp = None

        for i in people:
            if i.isLoggedOn is True:
                return "User already logged in"
            if i.email == email:
                temp = i

        if temp is None:
            return "Invalid login info"
        elif temp.email != email or temp.password != password:
            return "Invalid login info"
        models.ModelPerson.objects.filter(email=email).update(isLoggedOn=True)
        return "Login successful"

    def logout(self):

        person = models.ModelPerson.objects.get(email=self.email)
        if person.isLoggedOn is False:
            return False
        models.ModelPerson.objects.filter(email = self.email).update(isLoggedOn=False)
        return True
