import calendar, random

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from backend.models import Inventory
from backend.models import Vendor
from backend.models import Sale_Site
from backend.models import Sale
from backend.models import Employee
from backend.models import Shift
from backend.models import Product_Type
from backend.models import Condition

from backend.forms import InventoryForm

# chart functions
def labor_costs():
    labor_costs = 0
    for shift in Shift.objects.all():
        labor_costs += shift.money
    return labor_costs

def total_sales():
    total_sales = 0
    for sale in Sale.objects.all():
        total_sales += sale.sel_price
    return total_sales

def category_sales():
    category_sales = {}

    for s in Sale.objects.all():
        if category_sales.get(s.product_type) is None:
            category_sales[s.product_type] = s.sel_price
        else:
            category_sales[s.product_type] += s.sel_price

    return category_sales
 
def colors(n):
  ret = []
  r = int(random.random() * 256)
  g = int(random.random() * 256)
  b = int(random.random() * 256)
  step = 256 / n
  for i in range(n):
    r += step
    g += step
    b += step
    r = int(r) % 256
    g = int(g) % 256
    b = int(b) % 256
    a = 0.5
    ret.append((r,g,b,a)) 
  return ret
#end chart functions

@login_required
def dashboard(request):
    if request.method == 'POST':
        pass
    return render(request, 'dashboard.html', {
    })


@login_required
def employee(request):
    emp = get_object_or_404(Employee, user=request.user)
    open_shifts = Shift.objects.filter(emp_ID=emp, time_out__isnull=True)

    # Dictionary of stuff that should always be included in the
    # render context
    base_context = {
        "labor_cost" : labor_costs(),
        "total_sales": total_sales(),
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


@login_required
def inventory(request):
    if request.method == 'POST':
        entry = InventoryForm(request.POST)
        if entry.is_valid():
            entry.save()
    return render(request, 'inventory.html', {
        "items": Inventory.objects.all(),
        "vendors": Vendor.objects.all(),
        "channels": Sale_Site.objects.all(),
        "employee": Employee.objects.all(),
        "shift": Shift.objects.all(),
        "product_types": Product_Type.objects.all(),
        "conditions": Condition.objects.all(),
    })

@login_required
def delete_inventory(request):
    if request.method == 'POST':
        form = Inventory()
        inventory = Inventory.objects.all()
        item_id = request.POST.get('product_code')
        item = Inventory.objects.get(product_code=item_id)
        item.delete()
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
def reports(request):
    if request.method == 'POST':
        pass
    return render(request, 'reports.html', {
        "sales": Sale.objects.all()      
        })

@login_required
def sales(request):
    if request.method == 'POST':
        pass
    cs = category_sales()
    cs_colors = colors(len(cs))
    return render(request, 'sales.html', {
        "total_sales": total_sales(),
        "cat_sal": cs,
        "color": cs_colors
    })

