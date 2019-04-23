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
            return_string = "Invalid command."

            some_person = self.whos_logged_in()

            if first_parse != "login" and some_person is None:
                return "Please login first."

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

            elif first_parse == "change_email":
                return_string = self.change_email(parse_cmd)

            elif first_parse == "change_password":
                return_string = self.change_password(parse_cmd)

            elif first_parse == "change_name":
                return_string = self.change_name(parse_cmd)

            elif first_parse == "change_phone":
                return_string = self.change_phone(parse_cmd)

            elif first_parse == "view_info":
                return_string = self.view_info(parse_cmd)

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
        if not parse_cmd[2].isdigit():
            return "An error occurred"
        if current_user.type == "administrator":
            adm = Administrator(current_user.email, current_user.password, current_user.type)
            if adm.create_course(parse_cmd[1], int(parse_cmd[2])):
                return "Course has been created successfully."
            else:
                return "An error occurred"
        elif current_user.type == "supervisor":
            sup = Supervisor(current_user.email, current_user.password, current_user.type)
            if sup.create_course(parse_cmd[1], int(parse_cmd[2])):
                return "Course has been created successfully."
            else:
                return "An error occurred"
        else:
            return "Yeah, you don't have access to that command. Nice try buddy."

    def create_account(self, parse_cmd):
        # Jeff's method
        # calls create_account for admin and supervisor

        some_guy = self.whos_logged_in()

        if len(parse_cmd) != 4:
            return "Parameter error."

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
        # Jeff's method
        # calls edit_account for admin and supervisor

        current_user = self.whos_logged_in()
        fail_string = "Invalid command"

        if current_user.type != "administrator" and current_user.type != "supervisor":
            return fail_string

        if len(parse_cmd) < 4:
            return fail_string

        if parse_cmd[2] == "name" and len(parse_cmd) > 3:
            i = 4
            while i < len(parse_cmd):
                parse_cmd[3] = parse_cmd[3] + " " + parse_cmd[i]
                i = i + 1
        else:
            if len(parse_cmd) != 4:
                return fail_string

        if current_user.type == "administrator":
            admin1 = Administrator(current_user.email, current_user.password, current_user.type)
            did_work = admin1.edit_account(parse_cmd[1], parse_cmd[2], parse_cmd[3])
        else:
            super1 = Supervisor(current_user.email, current_user.password, current_user.type)
            did_work = super1.edit_account(parse_cmd[1], parse_cmd[2], parse_cmd[3])

        if did_work:
            return "Command successful."
        else:
            return "Command error."

    def access_info(self, parse_cmd):
        # Jeff's method
        # calls access_info for admin and supervisor

        info = "Invalid command."
        some_guy = self.whos_logged_in()

        if len(parse_cmd) != 1 or some_guy is None:
            return info

        if some_guy.type == "administrator":
            admin = Administrator(some_guy.email, some_guy.password, some_guy.type)
            info = admin.access_info()
        elif some_guy.type == "supervisor":
            sup = Supervisor(some_guy.email, some_guy.password, some_guy.type)
            info = sup.access_info()

        return info

    def assign_instructor(self, parse_cmd):
        if len(parse_cmd) != 3:
            return "Incorrect Command"
        temp = self.whos_logged_in()
        if temp.type == "administrator" or temp.type == "instructor" or temp.type == "ta":
            return "Access Denied"
        some_guy = Supervisor(temp.email, temp.password, temp.type)
        try:
            check_ins = models.ModelPerson.objects.get(email=parse_cmd[1], type="instructor")
        except models.ModelPerson.DoesNotExist:
            check_ins = None
        if check_ins is None:
            return "no such instructor"
        try:
            check_course = models.ModelCourse.objects.get(course_id=parse_cmd[2])
        except models.ModelCourse.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        if some_guy.assign_instructor(check_ins, check_course):
            return "command successful"
        else:
            return "command unsuccessful"

    def assign_ta(self, parse_cmd):
        if len(parse_cmd) != 3:
            return "Incorrect Command"
        temp = self.whos_logged_in()
        if temp is None:
            return "Incorrect Command"
        if temp.type != "supervisor":
            return "Access Denied"
        try:
            check_ta = models.ModelPerson.objects.get(email=parse_cmd[1], type="ta")
        except models.ModelPerson.DoesNotExist:
            check_ta = None
        if check_ta is None:
            return "no such ta"
        try:
            check_course = models.ModelCourse.objects.get(course_id=parse_cmd[2])
        except models.ModelCourse.DoesNotExist:
            check_course = None
        if check_course is None:
            return "no such course"

        some_guy = Supervisor(temp.email, temp.password, temp.type)
        if some_guy.assign_ta_course(check_ta, check_course):
            return "command successful"
        else:
            return "command unsuccessful"

    def view_ta_assign(self, parse_cmd):
        current_user = self.whos_logged_in()

        if len(parse_cmd) != 1:
            return "View TA assignments not of the right format: [view_ta_assign]"
        if current_user.type == "ta":
            tee_ayy = TA(current_user.email, current_user.password, current_user.type)
            return tee_ayy.view_ta_assignments()
        if current_user.type == "instructor":
            instructor = Instructor(current_user.email, current_user.password, current_user.type)
            return instructor.view_ta_assign()
        else:
            return "You don't have access to that command."

    def change_email(self, parse_cmd):

        some_guy = self.whos_logged_in()

        if len(parse_cmd) != 2:
            return "Parameter error."

        person = Person(some_guy.email, some_guy.password, some_guy.type)
        did_work = person.change_email(parse_cmd[1])

        if did_work:
            return "Email address changed."
        else:
            return "Invalid/taken email address."

    def change_password(self, parse_cmd):

        some_guy = self.whos_logged_in()

        if len(parse_cmd) != 2:
            return "Parameter error."

        person = Person(some_guy.email, some_guy.password, some_guy.type)
        did_work = person.change_password(parse_cmd[1])

        if did_work:
            return "Password changed."
        else:
            return "Bad password."

    def change_name(self, parse_cmd):

        some_guy = self.whos_logged_in()

        if len(parse_cmd) < 2:
            return "Parameter error."

        person = Person(some_guy.email, some_guy.password, some_guy.type)

        name_length = len(parse_cmd)
        i = 2
        some_name = parse_cmd[1]

        while i < name_length:
            some_name = some_name + " " + parse_cmd[i]
            i = i + 1

        did_work = person.change_name(some_name)

        if did_work:
            return "Name changed."
        else:
            return "Bad name."

    def change_phone(self, parse_cmd):

        some_guy = self.whos_logged_in()

        if len(parse_cmd) != 2:
            return "Parameter error."

        person = Person(some_guy.email, some_guy.password, some_guy.type)
        did_work = person.change_phone(parse_cmd[1])

        if did_work:
            return "Phone number changed."
        else:
            return "Invalid phone format."

    def view_info(self, parse_cmd):

        some_guy = self.whos_logged_in()

        if len(parse_cmd) != 1:
            return "Parameter error."

        person = Person(some_guy.email, some_guy.password, some_guy.type)
        return person.view_info()
