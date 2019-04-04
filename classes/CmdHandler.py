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
        return True

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
