from classes.Administrator import Administrator
from classes.Course import Course
from classes.Instructor import Instructor
from classes.Person import Person
from classes.Supervisor import Supervisor
from classes.TA import TA

from ta_assign import models

# importing all the things, because who knows


class CmdHandler:

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

    def whos_logged_in(self):
        try:
            some_person = models.ModelPerson.objects.get(isLoggedOn=True)
        except models.ModelPerson.DoesNotExist:
            return None

        return some_person

    def parse_command(self, some_cmd):
        # if we don't have an admin yet
        if not self.check_setup():
            # if we didn't type setup, tell them to setup
            if some_cmd != "setup":
                return "Please run setup before attempting to execute commands."
            # create a new admin
            else:
                setup_string = self.setup()
                return setup_string
        else:
            parse_cmd = some_cmd.split()
            first_parse = parse_cmd[0]
            return_string = ""

            if first_parse == "login":
                return_string = self.login(parse_cmd)

            elif first_parse == "logout":
                return_string = self.logout(parse_cmd)

            elif first_parse == "create_course":
                return_string = self.create_course(parse_cmd)

            elif first_parse == "create_account":
                return_string = self.create_account(parse_cmd)

            elif first_parse == "edit_account":
                return_string = self.edit_account(parse_cmd)

            elif first_parse == "access_info":
                return_string = self.access_info(parse_cmd)

            elif first_parse == "assign_instructor":
                return_string = self.assign_instructor(parse_cmd)

            elif first_parse == "assign_ta":
                return_string = self.assign_ta(parse_cmd)

            elif first_parse == "view_ta_assign":
                return_string = self.view_ta_assign(parse_cmd)

            else:
                return "I don't even know what the heck you just wrote. Do it again but better."

            return return_string

    def login(self, parse_cmd):
        if len(parse_cmd) != 3:
            return "Incorrect Command"
        return Person.login(parse_cmd[1], parse_cmd[2])

    def logout(self, parse_cmd):
        if len(parse_cmd) != 1:
            return "Incorrect Command"
        temp = self.whos_logged_in()
        if temp is None:
            return "Incorrect Command"

        person = Person(temp.email, temp.password, temp.type)
        return person.logout()

    def create_course(self, parse_cmd):
        current_user = self.whos_logged_in()
        if len(parse_cmd) != 3:
            return "Command not of the right format: [create_course CS###-### #]"
        if current_user.type == "administrator":
            adm = Administrator(current_user.email, current_user.password, current_user.type)
            if adm.create_course(parse_cmd[1], int(parse_cmd[2])):
                return parse_cmd[1]+" has been created successfully."
            else:
                return "An error occurred"
        elif current_user.type == "supervisor":
            sup = Supervisor(current_user.email, current_user.password, current_user.type)
            if sup.create_course(parse_cmd[1], int(parse_cmd[2])):
                return parse_cmd[1] + " has been created successfully."
            else:
                return "An error occurred"
        else:
            return "Yeah, you don't have access to that command. Nice try buddy."

    def create_account(self, parse_cmd):
        some_guy = self.whos_logged_in()

        if len(parse_cmd) != 4:
            return "Invalid command."

        if some_guy.type == "administrator":
            admin = Administrator(some_guy.email, some_guy.password, some_guy.type)
            did_work = admin.create_account(parse_cmd[1], parse_cmd[2], parse_cmd[3])
        elif some_guy.type == "supervisor":
            sup = Supervisor(some_guy.email, some_guy.password, some_guy.type)
            did_work = sup.create_account(parse_cmd[1], parse_cmd[2], parse_cmd[3])
        else:
            return "Invalid command."

        if did_work:
            return "Account created!"
        else:
            return "Account creation error."

    def edit_account(self, parse_cmd):
        current_user = self.whos_logged_in()

        if parse_cmd[2] == "name":
            name = ' '.join(parse_cmd[3:])
            if current_user.type == "administrator":
                adm = Administrator(current_user.email, current_user.password, current_user.type)
                if adm.edit_account(current_user.email, parse_cmd[1], name):
                    return "User's name has been changed successfully"
                else:
                    return "An error occurred"
            elif current_user.type == "supervisor":
                sup = Supervisor(current_user.email, current_user.password, current_user.type)
                if sup.edit_account(current_user.email, parse_cmd[1], name):
                    return "User's name has been changed successfully"
                else:
                    return "An error occurred"
            else:
                return "Yeah, you don't have access to that command. Nice try buddy."
        elif parse_cmd[2] == "email":
            if len(parse_cmd) != 4:
                return "Command not of the right format: [edit_account field content]"
            if current_user.type == "administrator":
                adm = Administrator(current_user.email, current_user.password, current_user.type)
                if adm.edit_account(current_user.email, parse_cmd[2], parse_cmd[3]):
                    return "User's email has been changed successfully"
                else:
                    return "An error occurred"
            elif current_user.type == "supervisor":
                sup = Supervisor(current_user.email, current_user.password, current_user.type)
                if sup.create_course(parse_cmd[2], int(parse_cmd[3])):
                    return "User's " + parse_cmd[2] + " has been changed successfully"
                else:
                    return "An error occurred"
            else:
                return "Yeah, you don't have access to that command. Nice try buddy."
        elif parse_cmd[2] == "password":
            if len(parse_cmd) != 4:
                return "Command not of the right format: [edit_account field content]"
            if current_user.type == "administrator":
                adm = Administrator(current_user.email, current_user.password, current_user.type)
                if adm.edit_account(current_user.email, parse_cmd[2], parse_cmd[3]):
                    return "User's email has been changed successfully"
                else:
                    return "An error occurred"
            elif current_user.type == "supervisor":
                sup = Supervisor(current_user.email, current_user.password, current_user.type)
                if sup.create_course(parse_cmd[2], int(parse_cmd[3])):
                    return "User's " + parse_cmd[2] + " has been changed successfully"
                else:
                    return "An error occurred"
            else:
                return "Yeah, you don't have access to that command. Nice try buddy."
        elif parse_cmd[2] == "phone":
            if len(parse_cmd) != 4:
                return "Command not of the right format: [edit_account field content]"
            if current_user.type == "administrator":
                adm = Administrator(current_user.email, current_user.password, current_user.type)
                if adm.edit_account(current_user.email, parse_cmd[2], parse_cmd[3]):
                    return "User's email has been changed successfully"
                else:
                    return "An error occurred"
            elif current_user.type == "supervisor":
                sup = Supervisor(current_user.email, current_user.password, current_user.type)
                if sup.create_course(parse_cmd[2], int(parse_cmd[3])):
                    return "User's " + parse_cmd[2] + " has been changed successfully"
                else:
                    return "An error occurred"
            else:
                return "Yeah, you don't have access to that command. Nice try buddy."
        else:
            return "That wasn't a very good account field."

    def access_info(self, parse_cmd):

        if len(parse_cmd) != 1:
            return "Invalid command."

        some_guy = self.whos_logged_in()
        info = []

        if some_guy.type == "administrator":
            admin = Administrator(some_guy.email, some_guy.password, some_guy.type)
            info = admin.access_info()
        elif some_guy.type == "supervisor":
            sup = Supervisor(some_guy.email, some_guy.password, some_guy.type)
            info = sup.access_info()

        return info

    def assign_instructor(self, parse_cmd):
        return

    def assign_ta(self, parse_cmd):
        return

    def view_ta_assign(self, parse_cmd):
        current_user = self.whos_logged_in()

        if len(parse_cmd) != 1:
            return "View TA assignments not of the right format: [view_ta_assign]"
        if current_user.type == "ta":
            tee_ayy = TA(current_user.email, current_user.password, current_user.type)
            tee_ayy.view_ta_assignments()
        if current_user.type == "instructor":
            instructor = Instructor(current_user.email, current_user.password, current_user.type)
            instructor.view_ta_assign()
        else:
            return "You don't have access to that command."
