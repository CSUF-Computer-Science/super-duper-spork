from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.models import Inventory
from backend.models import Vendor
from backend.models import Sale_Site
from backend.models import Employee
from backend.models import Shift

@login_required
def inventory(request):
    if request.method == 'POST':
        pass # TODO Implement form submission entries here

    return render(request, 'inventory.html', {
        "items": Inventory.objects.all(),
        "vendors": Vendor.objects.all(),
        "channels": Sale_Site.objects.all(),
        "employee": Employee.objects.all(),
        "shift": Shift.objects.all()
    })

def employee(request):
    return render(request, 'employees.html',{
        "employee": Employee.objects.all(),
        "shift": Shift.objects.all()
    })
