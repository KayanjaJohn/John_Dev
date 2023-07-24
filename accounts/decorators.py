from django.shortcuts import redirect
from django.http import HttpResponse

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_director == 'is_director':
                return redirect('directorDashboard')
            elif request.user.is_work_plan_manager == 'is_work_plan_manager':
                return redirect('workPlanManagerDashboard')
            elif request.user.is_manager == 'is_manager':
                return redirect('managerDashboard')
            else:
                return redirect('adminDashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def admin_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_director == 'is_director':
            return HttpResponse('You do not have access to this page')
        elif request.user.is_work_plan_manager == 'is_work_plan_manager':
            return HttpResponse('You do not have access to this page')
        elif request.user.is_manager == 'is_manager':
            return HttpResponse('You do not have access to this page')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func