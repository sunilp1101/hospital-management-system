from django import forms
from django.contrib.auth.forms import UserCreationForm
from hospital.models import PatientRegistration,User,Patient,Doctor,Appointment,Drugs,Billing,Invoice,PatientMedicine




class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model= PatientRegistration

        exclude=[ 'status' ]
        widgets = {

                    'patient_title': forms.Select(attrs={'class': 'form-control'}),
                    'patient_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Patient Name'}),
                    'patient_age': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Age'}),
                    'patient_gender': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Gender'}),
                    'patient_phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Phone Number'}),
                    'patient_address': forms.Textarea(attrs={'class': 'form-control','rows': 3,'placeholder': 'Enter Address'}),
                    'doctor': forms.Select(attrs={'class': 'form-select'}),
                    'appointment_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
                    'appointment_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),

        }
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.IntegerField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields=[
            'username',
            'first_name',
            'last_name',
            'age',
            'phone_number',
            'email',
            'password1',
            'password2',
        ]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs['class']='form-control'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields='__all__'

        widgets = {
            'patient_title' : forms.Select(attrs={'class': 'form-control'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-control' }),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'patient_gender': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_address': forms.Textarea(attrs={'class': 'form-control','rows': 3 }),

        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

        widgets = {
            'doctor_title': forms.Select(attrs={'class': 'form-control'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor_specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields='__all__'

        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor' : forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'appointment_status': forms.Select(attrs={'class': 'form-select'}),
            'appointment_method': forms.Select(attrs={'class': 'form-select'}),
        }
class DrugsForm(forms.ModelForm):
    class Meta:
        model = Drugs
        fields='__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Drug Name'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Manufacturer Name'}),
            'manufactured_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Quantity'}),
            'price':forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Price','step':'0.01','min':'0'}),
        }

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields='__all__'
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'medicine_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'lab_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),

        }

class PatientMedicineForm(forms.ModelForm):
    class Meta:
        model = PatientMedicine
        fields = ['drug','quantity']
        widgets = {
            'patient':forms.Select(attrs={'class': 'form-control'}),
            'drug':forms.Select(attrs={'class': 'form-control'}),
            'quantity':forms.NumberInput(attrs={'class': 'form-control','min':'1'}),
        }
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['billing']

        widgets = {
            'billing': forms.Select(attrs={'class': 'form-select'}),
        }