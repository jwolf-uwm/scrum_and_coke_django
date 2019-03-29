# created by Grant


class Person:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.phone_number = -1
        self.name = "DEFAULT"
        self.isLoggedIn = False

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

        if self.email != email | self.password != password:
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
