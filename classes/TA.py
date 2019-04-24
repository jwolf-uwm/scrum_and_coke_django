# created by Dillan

from classes.Person import Person
from ta_assign import models


class TA(Person):

    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)

    def view_ta_assignments(self):
        string_list = "TA: "
        tee_ayys = models.ModelPerson.objects.filter(type="ta")
        for tee_ayy in tee_ayys:
            string_list = string_list + tee_ayy.name + " | " + tee_ayy.email + "\n"

            for ta_courses in models.ModelTACourse.objects.all():
                if ta_courses.TA.email == tee_ayy.email:
                    string_list = string_list + "Course: " + ta_courses.course.course_id + "\n"

        return string_list

    def read_public_contact(self, class_list):
        return

    def edit_contact_info(self, field, content):
        return
