from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView, UpdateView
from telecaller import forms
from telecaller.models import Enquires
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView,CreateView,ListView
from datetime import date
from django.utils.decorators import method_decorator
from telecaller.decoratores import signin_required


@method_decorator(signin_required,name="dispatch")
class TellecallersHome(TemplateView):
    template_name="TeleHome.html"

class SignInView(TemplateView):
    def get(self,request,*args,**kwargs):
        form=forms.SignInForm
        context={"form":form}
        return render(request,"signin.html",context)
    
    def post(self,request,*args,**kwargs):
        form=forms.SignInForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user=authenticate(request,username=email,password=password)
            print("here -----")
            if (user):
                login(request,user)
                print(user)
                if (request.user.role=="telecaller"):
                    return render(request,"TeleHome.html")  
                else:             
                    return redirect("signin")
            else:
                print("unauthorized user")
        else:
            context={"form":form}
            return render(request,"signin.html",context)

                
def signout(request):
    logout(request)
    return redirect("signin")


@method_decorator(signin_required,name="dispatch")
class EnquireyAddView(CreateView):
    model=Enquires
    form_class=forms.EnquireyForm
    template_name="enquiry.html"
    success_message = "Enquiry added successfully"
    success_url = reverse_lazy("telehome")
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            enquiry=form.save(commit=True)
            enquiry.created_by=request.user
            enquiry.save()
            return redirect("enquiryadd")

@method_decorator(signin_required,name="dispatch")
class EnquiryListVIew(ListView):
    model=Enquires
    template_name="enquirylist.html"
    context_object_name="enquires"
    def get_queryset(self):
        user=self.request.user
        return self.model.objects.filter(created_by=user)  

@method_decorator(signin_required,name="dispatch")
class EnquiryUpdate(UpdateView):
    model=Enquires
    pk_url_kwarg='id'
    form_class=forms.EnquireyForm
    template_name="enquiryupdate.html"
    success_url=reverse_lazy("enquirylist")

@method_decorator(signin_required,name="dispatch")
class EnquiryDelete(DeleteView):
    model=Enquires
    pk_url_kwarg='id'
    template_name="enquirydelete.html"
    success_url=reverse_lazy("enquirylist")

@method_decorator(signin_required,name="dispatch")
class FollowUpsView(ListView):
    model=Enquires
    template_name="followup.html"
    context_object_name="followups"
    def get_queryset(self):
        user=self.request.user
        return self.model.objects.filter(created_by=user,followup_date=date.today())

@method_decorator(signin_required,name="dispatch")
class ReportView(ListView):
    model=Enquires
    template_name="report.html"
    context_object_name="reports"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs) 
        user=self.request.user
        reportcount=self.model.objects.filter(enquiry_date=date.today(),created_by=user).count()
        context["reports"]=reportcount
        admissioncount=self.model.objects.filter(enquiry_date=date.today(),created_by=user,status="admitted").count()
        context["admissioncount"]=admissioncount
        form=forms.DateFilterForm()
        context["form"]=form
        return context
    def post(self,request,*args,**kwargs):
        form=forms.DateFilterForm(request.POST)
        if form.is_valid():
            from_date=form.cleaned_data["from_date"]
            to_date=form.cleaned_data["to_date"]
            admissioncount=Enquires.objects.filter(created_by=request.user,status="admitted",enquiry_date__range=[from_date,to_date]).count()
            enquirycount=Enquires.objects.filter(created_by=request.user,enquiry_date__range=[from_date,to_date]).count()
            context={}
            context["admissioncount"]=admissioncount
            context["enquirycount"]=enquirycount
            form=forms.DateFilterForm()
            context["form"]=form
            return render(request,self.template_name,context)