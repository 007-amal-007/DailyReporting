from django.urls import path
from telecaller import views

urlpatterns= [
    path("home",views.TellecallersHome.as_view(),name="telehome"),
    path("account/login",views.SignInView.as_view(),name="signin"),
    path("account/logout",views.signout,name="signout"),
    path("enquiry/add",views.EnquireyAddView.as_view(),name="enquiryadd"),
    path("enquiry/list",views.EnquiryListVIew.as_view(),name="enquirylist"),
    path("enquiry/update/<int:id>",views.EnquiryUpdate.as_view(),name="enquiryupdate"),
    path("enquiry/delete/<int:id>",views.EnquiryDelete.as_view(),name="enquirydelete"),
    path("enquiry/followups",views.FollowUpsView.as_view(),name="followups"),
    path("enquiry/reports",views.ReportView.as_view(),name="reports"),
]