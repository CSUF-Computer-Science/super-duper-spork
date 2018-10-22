from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.models import Inventory
from backend.models import Vendor
from backend.models import Sale_Site
from backend.models import Employee
from backend.models import Shift
from backend.models import Product_Type
from backend.models import Condition

from backend.forms import AddItemForm


@login_required
def inventory(request):
    if request.method == 'POST':
        entry = AddItemForm(request.POST)
        if entry.is_valid():
            entry.save()
        else:
            print("Bad sumbmission")

    return render(request, 'inventory.html', {
        "items": Inventory.objects.all(),
        "vendors": Vendor.objects.all(),
        "channels": Sale_Site.objects.all(),
        "employee": Employee.objects.all(),
        "shift": Shift.objects.all(),
        "product_types": Product_Type.objects.all(),
        "conditions": Condition.objects.all()
    })


def employee(request):
    return render(request, 'employees.html', {
        "employee": Employee.objects.all(),
        "shift": Shift.objects.all()
    })
