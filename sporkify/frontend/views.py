from django.shortcuts import render

from backend.models import Inventory

def inventory(request):
    return render(request, 'inventory.html', {
        "items": Inventory.objects.all()
    })
