from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied

from .models import Employee

def find_employee_or_404(user):
    emp = get_object_or_404(Employee, user=user)
    return emp

hr_login_required_test = user_passes_test(lambda u: True if find_employee_or_404(u).is_hr() else False, login_url="/not-allowed/")
def hr_login_required(view_func):
    decorated_view_func = login_required(hr_login_required_test(view_func))
    return decorated_view_func

supervisor_login_required_test = user_passes_test(lambda u: True if find_employee_or_404(u).is_supervisor() else False, login_url="/not-allowed/")
def supervisor_login_required(view_func):
    decorated_view_func = login_required(supervisor_login_required_test(view_func))
    return decorated_view_func

admin_login_required_test = user_passes_test(lambda u: True if find_employee_or_404(u).is_admin() else False, login_url="/not-allowed/")
def admin_login_required(view_func):
    decorated_view_func = login_required(admin_login_required_test(view_func))
    return decorated_view_func

def permission_context_processor(request):
    return {
        'is_hr': find_employee_or_404(request.user).is_hr(),
        'is_supervisor': find_employee_or_404(request.user).is_supervisor(),
        'is_warehouse_admin': find_employee_or_404(request.user).is_admin(),
    }