from django.shortcuts import redirect
def signin_required(funn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated() and request.user.role=="admin":
             return redirect("signin")
        else:
            return funn(request,*args,**kwargs)
    return wrapper

def admin_permission_required(fun):
    def wrapper(request,*args,**kwargs):
        if not request.user.role=="admin":
            return redirect("adminlogin")
        else:
            return fun(request,*args,**kwargs )
    return wrapper