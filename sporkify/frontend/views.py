from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.models import Inventory
from backend.models import Vendor
from backend.models import Sale_Site

@login_required
def inventory(request):
    return render(request, 'inventory.html', {
        "items": Inventory.objects.all(),
        "vendors": Vendor.objects.all(),
        "channels": Sale_Site.objects.all()
    })
