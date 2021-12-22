from django import forms
# from django.forms import fields, widgets
# from django.forms.widgets import PasswordInput
from telecaller.models import Enquires

class SignInForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class EnquireyForm(forms.ModelForm):
    class Meta:
        model=Enquires
        exclude=("enquiry_date","created_by")
        widgets= {
            "followup_date" :forms.DateInput(attrs={"type":"date","class":"form-control"}),
            "status":forms.Select(attrs={"class":"form-control"}),
            "course":forms.Select(attrs={"class":"form-control"}),
            'email':forms.EmailInput(attrs={"class":"form-control"}),
            'contact':forms.TextInput(attrs={"class":"form-control"}),
            'student_name':forms.TextInput(attrs={"class":"form-control"}),
        }

class DateFilterForm(forms.Form):
    from_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))
    to_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))
