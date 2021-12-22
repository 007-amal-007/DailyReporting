from django.db import models
# from telecaller.models import Enquires


class Course(models.Model):
    course_name=models.CharField(max_length=20,unique=True)
    active_status=models.BooleanField(default=True)

    def __str__(self):
        return self.course_name

class Batch(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch_name=models.CharField(max_length=120,unique=True)
    active_status=models.BooleanField(default=True)


# class Enrolled(models.Model):
#     enroll_startdate=models.DateField(null=True)
#     enroll_enddate=models.DateField(null=True)
#     student=models.ForeignKey(Enquires,on_delete=models.CASCADE)
#     options=(
#         ("enrolled","enrolled"),
#         ("completed","completed"),
#         ("dropped","dropped")
#     )
#     course=models.ForeignKey(Course,on_delete=models.CASCADE)
#     status=models.CharField(max_length=50,choices=options,default="enrolled")