from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age=models.PositiveIntegerField()
    phone_number=models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    class Meta:
        db_table = "UserProfile"

class PatientRegistration(models.Model):
    title_choices = [('Mr', 'Mr'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.'),]
    patient_title = models.CharField(max_length=10, choices=title_choices, default='')
    patient_name = models.CharField(max_length=100)
    patient_age = models.IntegerField()
    patient_gender = models.CharField(max_length=10)
    patient_phone = models.CharField(max_length=15)
    patient_address = models.TextField()

    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_title} {self.patient_name}"

    class Meta:
        db_table = "PatientRegistration"

class Patient(models.Model):
    title_choices=[('Mr','Mr'), ('Mrs.', 'Mrs.'),('Ms.', 'Ms.'),('Dr.', 'Dr.'),]
    patient_title = models.CharField(max_length=10, choices=title_choices, default='')
    patient_name=models.CharField(max_length=20)
    patient_age=models.IntegerField()
    patient_gender=models.CharField(max_length=12)
    patient_phone=models.CharField(max_length=15)
    patient_address=models.TextField()


    def __str__(self):
        return f"{self.patient_title} {self.patient_name}"
    class Meta:
        db_table="Patient"

class Doctor(models.Model):
    title_choices = [('Dr.', 'Dr.'),('Prof.','Prof.'),]
    doctor_title = models.CharField(max_length=10, choices=title_choices, default='')
    doctor_name=models.CharField(max_length=20)
    doctor_specialization=models.CharField(max_length=50)
    doctor_phone=models.CharField(max_length=15)
    doctor_email=models.EmailField()



    def __str__(self):
        return f"{self.doctor_title} {self.doctor_name}"
    class Meta:
        db_table="Doctor"

class Appointment(models.Model):

    appointment_choices=(('online','Online'),('offline','Offline'))
    status_choices=(('pending','Pending'),('completed','Completed'),('cancelled','cancelled'))
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    appointment_date=models.DateField()
    appointment_time=models.TimeField()
    appointment_status=models.CharField(max_length=20,choices=status_choices,default='pending')
    appointment_method=models.CharField(max_length=10,choices=appointment_choices,default='online')
    def __str__(self):
        return f"{self.patient} - {self.doctor}"
    class Meta:
        db_table="Appointments"

class Drugs(models.Model):

    name=models.CharField(max_length=100)
    manufacturer=models.CharField(max_length=100)
    manufactured_date=models.DateField()
    expiry_date=models.DateField()
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name
    class Meta:
        db_table="Drugs"


class Billing(models.Model):

        payment_choices = [('Cash', 'Cash'),('UPI', 'UPI'),('Card', 'Card'),]
        payment_status= [('Pending', 'Pending'),('Paid', 'Paid'),]


        patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
        doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)

        consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        medicine_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

        total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

        payment_method = models.CharField(max_length=20, choices=payment_choices)
        payment_status=models.CharField(max_length=10, choices=payment_status,default='pending')
        billing_date = models.DateField(auto_now_add=True)

        def save(self, *args, **kwargs):
            self.total_amount = (self.consultation_fee +self.medicine_fee +self.lab_fee +self.other_fee)
            super().save(*args, **kwargs)

        def __str__(self):
            return f"Bill - {self.patient.patient_title} {self.patient.patient_name}"

        class Meta:
            db_table ="Billing"

class PatientMedicine(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    drug=models.ForeignKey(Drugs,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField(auto_now_add=True)

    def medicine_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.patient.patient_name} - {self.drug.name}"

    class Meta:
        db_table = "PatientMedicine"


class Invoice(models.Model):
    billing = models.OneToOneField(Billing, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    invoice_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.invoice_number:
            last = Invoice.objects.order_by('-id').first()

            if last:
                number = int(last.invoice_number.split('-')[1]) + 1
            else:
                number = 1

            self.invoice_number = f"INV-{number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

    class Meta:
         db_table="Invoice"

