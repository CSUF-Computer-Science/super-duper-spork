"""sporkify URLS BEFORE GURLS Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from frontend import views

urlpatterns = [
    path('', views.inventory),
    path('add-item/', views.inventory),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard),
    path('delete-item/', views.delete_inventory),
    path('download-csv/', views.download_csv),
    path('employees/', views.employee),
    path('employees/create/', views.create_employee),
    path('employees/edit/', views.edit_employee),
    path('inventory/', views.inventory),
    path('not-allowed/', views.not_allowed),
    path('reports/', views.reports),
    path('sales/', views.sales),
    path('vendors/', views.vendors),
    path('download-csv-vendors/', views.download_csv_vendors),
    path('download-csv-timesheet/', views.download_csv_timesheet),
    path('download-csv-employees/', views.download_csv_employees)

]
