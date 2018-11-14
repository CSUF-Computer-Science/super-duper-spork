from django.forms import ModelForm
from backend.models import Inventory
from backend.models import Vendor
from backend.models import Sale
from backend.models import Open_Product_Code

class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ["product_code", "selling_site", "vendor", "condition", "pur_price", "ask_price", "product_type",
                  "added_by"]

class AddVendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ["comp_Name", "contact_name", "contact_phone", "contact_email"]
