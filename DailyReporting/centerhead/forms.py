from django.forms import ModelForm, fields, widgets
from django import forms
from centerhead.models import Course,Batch
from drs.models import MyUser

class CourseForm(ModelForm):
    class Meta:
        model=Course
        fields=["course_name"]
        widgets= {
            'course_name':widgets.TextInput(attrs={"class":"form-control"})
        }

class BatchForm(ModelForm):
    class Meta:
        model=Batch
        fields=["course","batch_name"]
        widgets={
            'course':widgets.Select(attrs={"class":"form-control"}),
            'batch_name':widgets.TextInput(attrs={"class":"form-control"}),
        }

class EmployeeForm(ModelForm):
    class Meta:
        model=MyUser
        fields=["email","phone","role","password"]
        widgets={
            'email':widgets.EmailInput(attrs={"class":"form-control"}),
            'phone':widgets.NumberInput(attrs={"class":'form-control'}),
            'role':widgets.Select(attrs={"class":"form-control"}),
            'password':widgets.PasswordInput(attrs={"class":"form-control"}),
        }

class AdminLoginInForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))