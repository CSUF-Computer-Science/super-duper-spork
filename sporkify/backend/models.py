from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import timedelta

class Open_Product_Code(models.Model):
    product_code = models.CharField(max_length=15, primary_key=True, unique=True)
    slot_Size = models.ForeignKey('Slot_size', on_delete = models.SET_NULL, null=True)

class Slot_size(models.Model):
    size_title = models.CharField(max_length=15, primary_key=True, unique=True)
    size_volume = models.FloatField()

class Vendor(models.Model):
    comp_Name = models.CharField(max_length=100, unique=True, primary_key=True)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=50)
    contact_email = models.EmailField(max_length=254)

class Inventory(models.Model):
    product_code = models.CharField(primary_key=True, unique=True, max_length=9)
    selling_site = models.ForeignKey('Sale_Site' , on_delete = models.SET_NULL, null=True)
    vendor = models.ForeignKey('Vendor', on_delete = models.SET_NULL, null=True)
    condition = models.ForeignKey('Condition',on_delete = models.SET_NULL, null=True)
    pur_price = models.FloatField()
    ask_price = models.FloatField()
    product_type = models.ForeignKey('Product_Type', on_delete = models.SET_NULL, null=True)
    added_by = models.ForeignKey('Employee',on_delete = models.SET_NULL, null=True)
    time_added = models.DateTimeField(auto_now=True)

    def create(self):
        self.time_added = timezone.now()
        self.save()

class Sale_Site(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    domain = models.URLField(max_length=200)

class Condition(models.Model):
    cond_Name = models.CharField(max_length=30, unique=True, primary_key=True)

class Sale(models.Model):
    invoice_num = models.AutoField(primary_key=True, unique=True)
    past_product_code = models.CharField(max_length=15)
    selling_site = models.URLField(max_length=200)
    vendor = models.CharField(max_length=100)
    condition = models.CharField(max_length=30)
    pur_price = models.FloatField()
    sel_price = models.FloatField()
    #merge product name and brand for product type in function
    product_type = models.CharField(max_length=150)
    added_by = models.IntegerField()
    time_added = models.DateTimeField()
    shipment_number = models.CharField(max_length=100)
    time_archived = models.DateTimeField()

    def create(self):
        self.time_archived = timezone.now()
        self.save()

class Product_Type(models.Model):
    type_ID = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=75)
    weight = models.FloatField()
    brand = models.CharField(max_length=75)

    def __str__(self):
        return self.type_name

class Employee(models.Model):
    EMPLOYEE = 1
    HR = 2
    SUPERVISOR = 3
    ADMIN = 4

    USER_TYPE_CHOICES = (
        (EMPLOYEE, 'employee'),         # Can clock in/out, view their own profile, and manage inventory
        (HR, 'hr'),                     # Can view other profiles and time tracking info
        (SUPERVISOR, 'supervisor'),     # Can do everything
        (ADMIN, 'admin'),               # Can do everything + more
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    hourly_wage = models.FloatField()

    # Permissions cascade, meaning, if someone is a SUPERVISOR
    # they are also considered HR and an EMPLOYEE
    def is_hr(self):
        return self.user_type == Employee.HR or self.is_supervisor()

    def is_supervisor(self):
        return self.user_type == Employee.SUPERVISOR or self.is_admin()

    def is_admin(self):
        return self.user_type == Employee.ADMIN

    # Obsolete
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=75)

class Shift(models.Model):
    emp_ID = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True)
    hourly_wage = models.FloatField()

    def create(self):
        self.time_in = timezone.now()
        self.save()

    @property
    def time_worked(self):
        if self.time_out == None:
            return timedelta(seconds=0)
        return (self.time_out - self.time_in)

    @property
    def money(self):
        return (self.time_worked.total_seconds() / 3600) * self.hourly_wage

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=100, primary_key=True, unique=True)
    shipment_cost = models.FloatField()
    materials_used = models.TextField()
    material_cost = models.FloatField()
    user_shipped = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    time_shipped = models.DateTimeField()

    def create(self):
        self.time_shipped = timezone.now()
        self.save()
