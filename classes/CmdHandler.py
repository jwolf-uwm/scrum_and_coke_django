from classes.Administrator import Administrator
from classes.Course import Course
from classes.Instructor import Instructor
from classes.Person import Person
from classes.Supervisor import Supervisor
from classes.TA import TA

from ta_assign import models

# importing all the things, because who knows


class CmdHandler:

    current_user = None
    logged_in = False

    def check_setup(self):
        # check if an administrator exists
        try:
            models.ModelPerson.objects.get(type="administrator")

        except models.ModelPerson.DoesNotExist:
            return False

        try:
            models.ModelPerson.objects.get(type="supervisor")

        except models.ModelPerson.DoesNotExist:
            return False

        return True

    def setup(self):
        new_admin = Administrator("ta_assign_admin@uwm.edu", "password", "administrator")
        new_super = Supervisor("ta_assign_super@uwm.edu", "password", "supervisor")
        return "Admin/Supervisor accounts setup!"

    # might not be all that useful
    def query_by_email(self, email_addy):
        # give an email address, get the info you need to instantiate in a tuple
        person_stuff = []

        try:
            some_person = models.ModelPerson.objects.get(email=email_addy)

        except models.ModelPerson.DoesNotExist:
            return person_stuff

        else:
            person_stuff.append(some_person.email)
            person_stuff.append(some_person.password)
            person_stuff.append(some_person.type)

            return person_stuff

    def parse_command(self, some_cmd):
        # if we don't have an admin yet
        if not self.check_setup():
            # if we didn't type setup, tell them to setup
            if some_cmd != "setup":
                return "Please run setup before attempting to execute commands."
            # create a new admin
            else:
                self.setup()

        else:
            parse_cmd = some_cmd.split()
            first_parse = parse_cmd[0]

            if first_parse == "login":
                self.login(some_cmd)

            elif first_parse == "logout":
                self.logout(some_cmd)

            elif first_parse == "create_course":
                self.create_course(parse_cmd)

            elif first_parse == "create_account":
                self.create_account(some_cmd)

            elif first_parse == "access_info":
                self.access_info(some_cmd)

            elif first_parse == "assign_instructor":
                self.assign_instructor(some_cmd)

            elif first_parse == "assign_ta":
                self.assign_ta(some_cmd)

            elif first_parse == "view_ta_assign":
                self.view_ta_assign(some_cmd)

            else:
                return "Command not found."

    def login(self, some_cmd):
        return

    def logout(self, some_cmd):
        return

    def create_course(self, parse_cmd):
        if len(parse_cmd) != 3:
            return "Create course not of the right format: [create_course CS###-### #]"
        if self.current_user.type == "administrator":
            adm = Administrator(self.current_user.email, self.current_user.password, self.current_user.type)
            adm.create_course(parse_cmd[1], int(parse_cmd[2]))
        elif self.current_user.type == "supervisor":
            sup = Supervisor(self.current_user.email, self.current_user.password, self.current_user.type)
            sup.create_course(parse_cmd[1], int(parse_cmd[2]))
        else:
            return "Yeah, you don't have access to that command. Nice try buddy."

    def create_account(self, some_cmd):
        return

    def access_info(self, some_cmd):
        return

    def assign_instructor(self, some_cmd):
        return

    def assign_ta(self, some_cmd):
        return

    def view_ta_assign(self, some_cmd):
        return

    """
    def deal_with_command(self, some_cmd):
        # if we don't have an admin yet
        if not self.check_setup():
            # if we didn't type setup, tell them to setup
            if some_cmd != "setup":
                return "Please run setup before attempting to execute commands."
            # create a new admin
            else:
                # do setup stuff here
                new_admin = Administrator("ta_assign_admin", "password", "administrator")
                new_super = Supervisor("ta_assign_super", "password", "supervisor")
                return "Admin/Supervisor accounts setup!"

        else:
            parse_cmd = some_cmd.split()
            # check login
            if not self.logged_in:
                if parse_cmd[0] != "Login":
                    return "You have to log in first dummy"
                else:
                    try:
                        find_person = models.ModelPerson.objects.get(email=parse_cmd[1])
                    except models.ModelPerson.DoesNotExist:
                        return f"The user {parse_cmd[1]} is not in the database"
                    if find_person.password != parse_cmd[2]:
                        return "The entered password is incorrect"
                    self.logged_in = True
                    self.current_user = find_person
                    return "Logged in successfully"

            # check logout
            if parse_cmd[0] == "Logout":
                self.logged_in = False
                return "Screw you guys, I'm going home"

            # check create_course
            if parse_cmd[0] == "create_course":
                if len(parse_cmd) != 3:
                    return "Create course not of the right format: create_course course_id num_labs"
                if self.current_user.type == "administrator":
                    adm = Administrator(self.current_user.email, self.current_user.password, self.current_user.type)
                    adm.create_course(parse_cmd[1], int(parse_cmd[2]))
                elif self.current_user.type == "supervisor":
                    sup = Supervisor(self.current_user.email, self.current_user.password, self.current_user.type)
                    sup.create_course(parse_cmd[1], int(parse_cmd[2]))
                else:
                    return "Yeah, you don't have access to that command. Nice try buddy."

            return "I don't even know what the heck you just wrote. Do it again but better."
    """
