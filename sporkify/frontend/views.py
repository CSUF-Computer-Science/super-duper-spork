import calendar

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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


@login_required
def employee(request):
    emp = get_object_or_404(Employee, user=request.user)
    open_shifts = Shift.objects.filter(emp_ID=emp, time_out__isnull=True)

    # Dictionary of stuff that should always be included in the
    # render context
    base_context = {
        "employees": Employee.objects.all(),    # List of employees
        "shifts": Shift.objects.all().order_by('-time_in'),                    # List of all shifts
        "myShifts": Shift.objects.filter(emp_ID=emp).order_by('-time_in'),     # List of user shifts
        "clockedIn": len(open_shifts) > 0       # If current user is clocked in
    }

    if base_context["clockedIn"]:
        cur_shift = open_shifts[0]
        base_context["curShiftStartedAt"] = calendar.timegm(cur_shift.time_in.utctimetuple())

    # Begin logic for the time clock
    if request.method == 'POST' and request.POST['clockInOut'] is not None:
        if len(open_shifts) == 0:
            # Create a new shift
            new_shift = Shift()
            new_shift.time_in = timezone.now()
            new_shift.emp_ID = emp
            new_shift.hourly_wage = emp.hourly_wage
            new_shift.save()

            return render(request, 'employees.html', {
                **base_context,
                "clockedInAt": timezone.now(),
                "curShiftStartedAt": calendar.timegm(timezone.now().utctimetuple()),
                "clockedIn": True  # Replace the initial clockedIn from above
            })
        elif len(open_shifts) == 1:
            # Close the open shift
            open_shift = open_shifts[0]
            open_shift.time_out = timezone.now()
            open_shift.save()

            secs = int(open_shift.time_worked.total_seconds())
            hours = int(secs // 3600)
            mins = int((secs - secs // 86400 - hours * 3600) // 60)

            return render(request, 'employees.html', {
                **base_context,
                "timeWorked": f"{hours:02}:{mins:02}:{secs:02}",
                "clockedIn": False  # Replace the initial clockedIn from above
            })
        else:  # More than one shift is open - this shouldn't happen
            raise Exception('More than one shift is open. How\'d you manage that?')

    return render(request, 'employees.html', base_context)
