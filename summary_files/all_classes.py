# created by Matt

from classes.Person import Person


class Administrator(Person):
    """
    an instance represents an administrator within the schools
    system
    must have username
    must have password
    must be able to create courses
    must be able to create accounts
    must be able to edit accounts
    must be able to delete account
    must be able to send notification
    must be able to access information
    """
    def __init__(self, email, password):
        self.password = password
        self.email = email

    def create_course(self, course_id, num_labs):
        return

    def create_account(self, email, password):
        return

    def edit_account(self, email, field, content):
        return

    def delete_account(self, email):
        return

    def send_notification(self, notification):
        return

    def access_info(self):
        return



class Course:
    def __init__(self, course_id, num_labs):
        self.course_id = course_id
        self.num_labs = num_labs
        # instructor should be a class at some point
        self.instructor = "Dr. Default"
        self.tee_ays = []

    def set_course_id(self, course_id):
        return

    def set_course_section(self, section_number):
        return

    def set_instructor(self, instructor):
        return

    def set_num_labs(self, lab_section):
        return

    def add_tee_ay(self, tee_ay):
        return

    def get_course_id(self):
        return

    def get_course_name(self):
        return

    def get_course_section(self):
        return

    def get_num_labs(self):
        return

    def get_tee_ays(self):
        return

# created by Jeff

from classes.Person import Person


class Instructor(Person):

    def __init__(self, email, password):
        super().__init__(email, password)

    def assign_ta_course(self, email, course_id, course_section):
        return

    def assign_ta_lab(self, email, lab_section):
        return

    def view_course_assign(self):
        return

    def read_public_contact(self):
        return

    def view_ta_assign(self):
        return

    def edit_contact_info(self, field, content):
        return

    def send_notification_ta(self, content):
        return

# created by Grant


class Person:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.phone_number = -1
        self.name = "DEFAULT"

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
        return

    def logout(self):
        return

# created by Evan

from classes.Person import Person


class Supervisor(Person):
    def __init__(self, email, password):
        super().__init__(email, password)

    def assign_instructor(self, email, course_id, section_id):
        """
        assigns the given instructor's course to the course parameter
        """
        return

    def assign_ta_course(self, email, course_id, course_section):
        """
        assigns the given TA's course to the course parameter
        """
        return

    def assign_ta_lab(self, email, course_id, lab_section):
        """
        assigns the given TA's lab
        """
        return

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
