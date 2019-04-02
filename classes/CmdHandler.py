from classes import Administrator
from classes import Course
from classes import Instructor
from classes import Person
from classes import Supervisor
from classes import TA
from ta_assign import models

# importing all the things, because who knows


class CmdHandler:

    current_user = None
    logged_in = False

    def check_setup(self):

        find_admin = models.ModelAdministrator.objects.all()

        if not find_admin.exists():
            return False

        else:
            return True

    def deal_with_command(self, some_cmd):

        if not self.check_setup():

            if some_cmd != "setup":
                return "Please run setup before attempting to execute commands."

            else:
                # do setup stuff here
                parse_cmd = some_cmd.split()
                if parse_cmd[0] == "create_course":
                    if len(parse_cmd) != 3:
                        return "Create course not of the right format: create_course course_id:String num_labs:Int"

                return "This will set stuff up someday."

        else:
            return "I'M HELPING LOOK: " + some_cmd
