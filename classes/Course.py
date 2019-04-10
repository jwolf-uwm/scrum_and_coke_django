from ta_assign import models

# Note these stubs are unimplemented as we are using calls from other classes to make
# courses right now. We have left them here in case we need them for future changes
# to the design or implementation.


class Course:
    def __init__(self, course_id, num_labs):
        self.course_id = course_id
        self.num_labs = num_labs
        # instructor should be a class at some point
        self.instructor = "not_set@uwm.edu"
        self.tee_ays = []

        some_course = models.ModelCourse()
        some_course.course_id = self.course_id
        some_course.num_labs = self.num_labs
        some_course.instructor = self.instructor
        # don't think there's any need to port over an empty list
        some_course.save()

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
