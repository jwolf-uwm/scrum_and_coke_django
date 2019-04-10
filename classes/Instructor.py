# created by Jeff
from classes.Person import Person
from ta_assign import models


class Instructor(Person):

    def __init__(self, email, password, account_type):
        super().__init__(email, password, account_type)

    def assign_ta_course(self, email, course_id, course_section):
        return

    def assign_ta_lab(self, email, lab_section):
        return

    def view_course_assign(self):
        return

    def read_public_contact(self):
        return

    def view_ta_assign(self):
        string_list = []
        tee_ayys = models.ModelPerson.objects.filter(type="ta")
        for tee_ayy in tee_ayys:
            # string_list.append("TA: " + tee_ayy.email)

            for ta_courses in models.ModelTACourse.objects.all():
                if ta_courses.TA.email == tee_ayy.email:
                    string_list.append("Course: " + ta_courses.course.course_id + " TA: " + ta_courses.TA.name + ", "
                                       + ta_courses.TA.email)

        return string_list

    def edit_contact_info(self, field, content):
        return

    def send_notification_ta(self, content):
        return
