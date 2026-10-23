from django.contrib import admin
from .models import UserProfile,Doctor,Patient,Appointment,Drugs,Billing,PatientMedicine

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Drugs)
admin.site.register(Billing)
admin.site.register(PatientMedicine)