from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.models import Inventory

@login_required
def inventory(request):
    return render(request, 'inventory.html', {
        "items": Inventory.objects.all()
    })
