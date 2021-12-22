from django.urls import path
from centerhead import views

urlpatterns = [
    path("drshome",views.AdminHome.as_view(),name="adminhome"),
    path("account/adminlogin",views.AdminLoginView.as_view(),name="adminlogin"),
    path("account/adminlogout",views.adminsignout,name="adminsingout"),
    path("courseadd",views.CourseAdd.as_view(),name="courseadd"),
    path("courseupdate/<int:id>",views.CourseUpdate.as_view(),name="courseupdate"),
    path("batchadd",views.BatchAdd.as_view(),name="batchadd"),
    path("batchupdate/<int:id>",views.BatchUpdateView.as_view(),name="batchupdate"),
    path("batchview/<int:id>",views.BatchDetailView.as_view(),name="bacthview"),
    path("employee",views.Employees.as_view(),name="employess"),
    path("employee/remove/<int:id>",views.EmployeeRemove.as_view(),name="empremove"),
    path("employee/update/<int:id>",views.EmployeeUpdate.as_view(),name="empupdate"),
    path("employee/detail/<int:id>",views.EmployeeDetail.as_view(),name="empdetail"),
    path("reports",views.ReportView.as_view(),name="viewreports"),
    path("datereports/",views.DateReport.as_view(),name="datereport"),
]
