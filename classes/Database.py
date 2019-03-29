from classes.Administrator import Administrator
from classes.Supervisor import Supervisor
from classes.Instructor import Instructor
from classes.TA import TA
from classes.Course import Course


class Database:

    def __init__(self):
        self.administrator = Administrator("admin@uwm.edu", "admin_password")
        self.supervisor = Supervisor("super@uwm.edu", "super_password")
        self.instructors = []
        self.tas = []
        self.courses = []

    def add_instructor(self, some_instructor):
        return

    def remove_instructor(self, some_instructor):
        return

    def add_ta(self, some_ta):
        return

    def remove_ta(self, some_ta):
        return

    def add_course(self, some_course):
        return

    def remove_course(self, some_course):
        return

    def show_all_users(self):
        return

    def show_all_courses(self):
        return

    def show_all(self):
        return
