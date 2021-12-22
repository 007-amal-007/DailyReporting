from django.db import models
from django.db.models.deletion import CASCADE
from centerhead.models import Course
from drs.models import MyUser

# Create your models here.

class Enquires(models.Model):
    student_name=models.CharField(max_length=120)
    contact=models.CharField(max_length=15)
    email=models.EmailField()
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    options=(
        ("admitted","admitted"),
        ("not-intrested","not-intrested"),
        ("followup","followup")
    )
    created_by=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=50,choices=options,default="followup")
    followup_date=models.DateField(null=True)
    enquiry_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student_name
