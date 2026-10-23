"""
URL configuration for hospital_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from django.urls import path
from hospital.views import patient_register,registration_view,login_view,logout_view,dashboard,home,patient_create,patient_update,patient_delete,patient_list,doctor_create,doctor_update,doctor_delete,doctor_list,appointment_create,appointment_update,appointment_delete,appointment_complete,appointment_cancel,appointment_list,appointment_details,drugs_create,drugs_update,drugs_delete,drugs_list,billing_create,billing_update,billing_delete,billing_list,invoice_detail,appointment_success,patient_medicine,patient_medicine_update,patient_medicine_delete,patient_medicine_list



urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient_register/',patient_register,name='patient_register'),
    path('appointment_success/',appointment_success,name='appointment_success'),
    path('register/',registration_view,name='register'),
    path('login/',login_view,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logout/',logout_view,name='logout'),
    path('',home,name='home'),
    path('patient_create/',patient_create,name="patient_create"),
    path('patient_update/<int:pk>/',patient_update,name='patient_update'),
    path('patient_delete/<int:pk>/',patient_delete,name='patient_delete'),
    path('patient_list/',patient_list,name='patient_list'),
    path('doctor_create/',doctor_create,name="doctor_create"),
    path('doctor_update/<int:pk>/',doctor_update,name='doctor_update'),
    path('doctor_delete/<int:pk>/',doctor_delete,name='doctor_delete'),
    path('doctor_list/',doctor_list,name='doctor_list'),
    path('appointment_create/',appointment_create,name="appointment_create"),
    path('appointment_update/<int:pk>/',appointment_update,name='appointment_update'),
    path('appointment_delete/<int:pk>/',appointment_delete,name='appointment_delete'),
    path('appointment_complete/<int:pk>/',appointment_complete,name='appointment_complete'),
    path('appointment_cancel/<int:pk>/',appointment_cancel,name='appointment_cancel'),
    path('appointment_list/',appointment_list,name='appointment_list'),
    path('appointment_detail/<int:pk>/',appointment_details,name='appointment_detail'),
    path('drugs_create/',drugs_create,name="drugs_create"),
    path('drugs_update/<int:pk>/',drugs_update,name='drugs_update'),
    path('drugs_delete/<int:pk>/',drugs_delete,name='drugs_delete'),
    path('drugs_list/',drugs_list,name='drugs_list'),
    path('billing_create/',billing_create,name="billing_create"),
    path('billing_update/<int:pk>/',billing_update,name='billing_update'),
    path('billing_delete/<int:pk>/',billing_delete,name='billing_delete'),
    path('billing_list/',billing_list,name='billing_list'),
    path('billing/<int:pk>/invoice/',invoice_detail,name='invoice_detail'),
    path('patient/<int:pk>/medicine/',patient_medicine,name='patient_medicine'),
    path('patient_medicine_update/<int:pk>/',patient_medicine_update,name='patient_medicine_update'),
    path('patient_medicine_delete/<int:pk>/',patient_medicine_delete,name='patient_medicine_delete'),
    path('patient_medicine_list/<int:pk>/',patient_medicine_list,name='patient_medicine_list'),

]
