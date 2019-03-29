from django.db import models


# Create your models here.
class Person(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.IntegerField(default=-1)
    name = models.CharField(max_length=50, default="DEFAULT")
    isLoggedOn = models.BooleanField(default=False)


class Administrator(Person):
    pass


class Supervisor(Person):
    pass


class TA(Person):
    pass


class Instructor(Person):
    pass


class Course(models.Model):
    course_id = models.CharField(max_length = 10)
    num_labs = models.IntegerField(default = 0)
    instructor = models.CharField(max_length=50)
    tee_ays = models.ForeignKey(TA, on_delete=models.CASCADE)
