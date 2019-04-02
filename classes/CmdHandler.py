from classes import Administrator
from classes import Course
from classes import Instructor
from classes import Person
from classes import Supervisor
from classes import TA
from ta_assign import models

# importing all the things, because who knows


class CmdHandler:
    @staticmethod
    def deal_with_command(some_cmd):

        return "I'M HELPING LOOK: " + some_cmd
