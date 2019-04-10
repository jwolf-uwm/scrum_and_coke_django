from django.db import models


# Create your models here.
class ModelPerson(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.IntegerField(default=-1)
    name = models.CharField(max_length=50, default="DEFAULT")
    type = models.CharField(max_length=20, default="person")
    isLoggedOn = models.BooleanField(default=False)


class ModelCourse(models.Model):
    course_id = models.CharField(max_length=10)
    num_labs = models.IntegerField(default=0)
    instructor = models.CharField(max_length=50, default="no Instructor")
    # temp disabled
    # tee_ays = models.ForeignKey(ModelTA, on_delete=models.CASCADE)


class ModelTACourse(models.Model):
    course = models.ForeignKey(ModelCourse, on_delete=models.CASCADE)
    TA = models.ForeignKey(ModelPerson, on_delete=models.CASCADE)
