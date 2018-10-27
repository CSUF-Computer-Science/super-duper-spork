from django.forms import ModelForm
from backend.models import Inventory


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ["product_code", "selling_site", "vendor", "condition", "pur_price", "ask_price", "product_type",
                  "added_by"]
