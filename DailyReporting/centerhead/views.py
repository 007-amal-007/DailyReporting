from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView,DeleteView, UpdateView,DetailView,ListView
from telecaller.models import Enquires
from centerhead.models import  Course,Batch
from centerhead import forms
from drs.models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from telecaller.forms import DateFilterForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from centerhead.decorators import admin_permission_required


class AdminLoginView(TemplateView):
    def get(self,request,*args,**kwargs):
        form=forms.AdminLoginInForm
        context={"form":form}
        return render(request,"centerhead/adminsignin.html",context)
    
    def post(self,request,*args,**kwargs):
        form=forms.AdminLoginInForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user=authenticate(request,username=email,password=password)
            if (user):
                login(request,user)
                if (request.user.role=="admin"):
                    print(request.user,"----------------")
                    return render(request,"centerhead/adminhome.html")
                elif (request.user.role=="superadmin"):
                    return redirect("superhome")   
                else:             
                    return redirect("adminlogin")
            else:
                print("else1")
                messages.error(request, 'Form submission FAil')
                return redirect("adminlogin")
        else:
            messages.error(request, 'Form submission FAil')
            print("else")
            return redirect("adminlogin")


def adminsignout(request):
    logout(request)
    return redirect("adminlogin")

@method_decorator(admin_permission_required,name="dispatch")
class AdminHome(TemplateView): 
    model=Enquires
    template_name="centerhead/adminhome.html"

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        notifications=Enquires.objects.filter(status="admitted").count()
        context["notifications"]=notifications
        print(context["notifications"])
        return context

@method_decorator(admin_permission_required,name="dispatch")
class CourseAdd(CreateView):
    model=Course
    form_class=forms.CourseForm
    template_name="centerhead/addcourse.html"
    success_url = reverse_lazy("courseadd")

    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(**kwargs)
        context["courses"]=self.model.objects.all()
        return context

@method_decorator(admin_permission_required,name="dispatch")
class CourseUpdate(UpdateView):
    model=Course
    form_class=forms.CourseForm
    template_name="centerhead/updatecourse.html"
    context_object_name="course"
    pk_url_kwarg='id'
    success_url=reverse_lazy("courseadd")

@method_decorator(admin_permission_required,name="dispatch")
class BatchAdd(CreateView):
    model=Batch
    form_class=forms.BatchForm
    tempate_name="centerhead/batch_form.html"
    success_url = reverse_lazy("batchadd")

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        context["batches"]=self.model.objects.all()
        return context
    

@method_decorator(admin_permission_required,name="dispatch")
class BatchUpdateView(UpdateView):
    model=Batch
    form_class=forms.BatchForm
    template_name="centerhead/updatebatch.html"
    pk_url_kwarg="id"
    success_url  = reverse_lazy("batchadd")

@method_decorator(admin_permission_required,name="dispatch")
class BatchDetailView(DetailView):
    model=Batch
    template_name="centerhead/viewbatch.html"
    context_object_name="batch"
    pk_url_kwarg="id"

@method_decorator(admin_permission_required,name="dispatch")
class BatchDeleteView(DeleteView):
    model=Batch
    template_name="centerhead/deletebatch.html"


@method_decorator(admin_permission_required,name="dispatch")
class Employees(CreateView):
    template_name="centerhead/employee.html"
    form_class= forms.EmployeeForm
    model=MyUser
    success_url = reverse_lazy("employess")

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["employees"]=self.model.objects.all()
        return context
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            employee=form.save(commit=False)
            emp=MyUser.objects.create_user(email=employee.email,phone=employee.phone,role=employee.role,password=employee.password)
            emp.save()
        return redirect("employess")

@method_decorator(admin_permission_required,name="dispatch")
class EmployeeUpdate(UpdateView):
    model=MyUser
    template_name="centerhead/updateemployee.html"
    form_class=forms.EmployeeForm
    pk_url_kwarg="id"
    success_url = reverse_lazy("employess") 


@method_decorator(admin_permission_required,name="dispatch")    
class EmployeeRemove(DeleteView):
    model=MyUser
    template_name="centerhead/remove.html"
    pk_url_kwarg="id"
    success_url = reverse_lazy("employess")

@method_decorator(admin_permission_required,name="dispatch")
class EmployeeDetail(DetailView):
    model=MyUser
    template_name="centerhead/emp_detail.html"
    pk_url_kwarg="id"
    context_object_name="employee"

@method_decorator(admin_permission_required,name="dispatch")
class ReportView(ListView):
    model=Enquires
    template_name="centerhead/report.html"
    context_object_name="enquiries"
    def get_context_data(self,*args,**kwargs): 
        context=super().get_context_data(**kwargs)
        report=Enquires.objects.all().values("created_by__email").annotate(enquiries=Count("created_by"))
        context["reports"]=report
        admissions=Enquires.objects.filter(status="admitted").values("created_by__email").annotate(admission_count=Count("created_by"))
        context["admissions"]=admissions
        return context

@method_decorator(admin_permission_required,name="dispatch")
class DateReport(ListView):
    model=Enquires
    template_name="centerhead/datereport.html"
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(**kwargs)
        form=DateFilterForm()
        context["form"]=form
        return context
        
    def post(self,request,*args,**kwargs):
        form=DateFilterForm(request.POST)
        if form.is_valid():
            from_date=form.cleaned_data["from_date"]
            to_date=form.cleaned_data["to_date"]
            datereport=Enquires.objects.filter(enquiry_date__range=[from_date,to_date],status="admitted").values("created_by__email","student_name").annotate(date_count=Count("created_by"))
            context={}
            context["datereport"]=datereport
            print(context["datereport"])
            form=DateFilterForm()
            context["form"]=form
            return render(request,self.template_name,context)