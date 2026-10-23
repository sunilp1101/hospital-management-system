from http.client import responses

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from hospital.models import UserProfile,Patient,PatientRegistration,Doctor,Appointment,Drugs,Billing,PatientMedicine,Invoice
from hospital.forms import PatientRegistrationForm,RegistrationForm,PatientForm,DoctorForm,AppointmentForm,DrugsForm,BillingForm,PatientMedicineForm



# Create your views here
def home(request):
    doctors= Doctor.objects.all()
    patients= Patient.objects.all()
    appointments= Appointment.objects.all()

    context={
        'doctors':doctors,
        'patients':patients,
        'appointments':appointments,
    }
    return render(request,'home.html',context)
@login_required
def dashboard(request):
    context={
        'patients':Patient.objects.count(),
        'doctors':Doctor.objects.count(),
        'appointments':Appointment.objects.count(),
        'Drugs':Drugs.objects.count(),
    }
    return render(request,'dashboard.html',context)
def patient_register(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)

        if form.is_valid():

            patient = Patient.objects.create(
                patient_title=form.cleaned_data['patient_title'],
                patient_name=form.cleaned_data['patient_name'],
                patient_age=form.cleaned_data['patient_age'],
                patient_gender=form.cleaned_data['patient_gender'],
                patient_phone=form.cleaned_data['patient_phone'],
                patient_address=form.cleaned_data['patient_address']
            )

            Appointment.objects.create(
                patient=patient,
                doctor=form.cleaned_data['doctor'],
                appointment_date=form.cleaned_data['appointment_date'],
                appointment_time=form.cleaned_data['appointment_time'],
                appointment_method='Online'
            )
            messages.success(request,"Your appointment has been registered successfully ")

            return redirect('appointment_success')
    else:
        form = PatientRegistrationForm()

    return render(request, 'patient_register.html', {'form': form})
def appointment_success(request):
    return render(request,'appointment_success.html')
@login_required
def registration_view(request):

    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                age=form.cleaned_data['age'],
                phone_number=form.cleaned_data['phone_number']
            )

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )
def login_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(
            request,username=username,
            password=password
        )
        if user is not None:
            login(request,user)
            return redirect('dashboard')

        return render(
            request,
            'login.html',
                      {'error':'Invalid Username or Password'}
        )
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def patient_create(request):
    if request.method=='POST':
        form=PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')

    else:
        form=PatientForm()
    return render(request,'patient_form.html',context={'form':form})

@login_required
def patient_update(request,pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form=PatientForm(request.POST,instance=patient)
        if form.is_valid():
            form.save()
            response=redirect('patient_list')
            return response
    else:
        form=PatientForm(instance=patient)
    return render(request,'patient_update.html',context={'form':form})

@login_required
def patient_delete(request,pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
            patient.delete()
            return redirect('patient_list')

    return render(request,'patient_delete.html',context={'patient':patient})

@login_required
def patient_list(request):
    patients= Patient.objects.all()
    return render(request,'patient_list.html',context={'patients':patients})

@login_required
def doctor_create(request):
    if request.method=='POST':
        form=DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')

    else:
        form=DoctorForm()
    return render(request,'doctor_form.html',context={'form':form})

@login_required
def doctor_update(request,pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'POST':
        form=DoctorForm(request.POST,instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')

    else:
        form=DoctorForm(instance=doctor)
    return render(request,'doctor_update.html',context={'form':form})

@login_required
def doctor_delete(request,pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'POST':
            doctor.delete()
            return redirect('doctor_list')

    return render(request,'doctor_delete.html',context={'doctor':doctor})

@login_required
def doctor_list(request):
    doctors=Doctor.objects.all()
    return render(request,'doctor_list.html',context={'doctors':doctors})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            appointment.appointment_method = 'Offline'

            appointment.save()

            return redirect('appointment_list')

    else:
        form = AppointmentForm()

    return render(request, 'appointment_form.html', {'form': form})
@login_required
def appointment_complete(request,pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.appointment_status = 'completed'
    appointment.save()
    return redirect('appointment_list')
@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == "POST":
            return redirect("appointment_list")
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, "appointment_form.html", {"form": form})

@login_required
def appointment_cancel(request,pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.appointment_status = 'cancelled'
    appointment.save()
    return redirect('appointment_list')

@login_required
def appointment_delete(request,pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
         appointment.delete()
         return redirect('appointment_list')

    return render(request,'appointment_delete.html',context={'appointment':appointment})

@login_required
def appointment_list(request):
    appointments=Appointment.objects.all()
    return render(request,'appointment_list.html',context={'appointments':appointments})

@login_required
def appointment_details(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        appointment.appointment_status = request.POST.get('appointment_status')
        appointment.appointment_method = request.POST.get('appointment_method')
        appointment.save()
        return redirect('appointment_list')

    return render( request,'appointment_detail.html',{'appointment': appointment})
@login_required
def drugs_create(request):
    if request.method=='POST':
        form=DrugsForm(request.POST)
        if form.is_valid():
             form.save()
             return redirect('drugs_list')

    else:
       form=DrugsForm()
    return render(request,'drugs_form.html',context={'form':form})

@login_required
def drugs_update(request,pk):
    drug = get_object_or_404(Drugs, pk=pk)

    if request.method == 'POST':
        form = DrugsForm(request.POST,instance=drug)

        if form.is_valid():
            form.save()
            return redirect('drugs_list')
    else:
        form = DrugsForm(instance=drug)
    return render(request,'drugs_update.html',{'form':form})
@login_required
def drugs_delete(request,pk):
    drug = get_object_or_404(Drugs, pk=pk)

    if request.method == 'POST':
        drug.delete()
        return redirect('drugs_list')

    return render(request,'drugs_delete.html',{'drug':drug})

@login_required
def drugs_list(request):
    drugs = Drugs.objects.all()
    return render(request,'drugs_list.html',context={'drugs':drugs})


@login_required
def billing_create(request):
    if request.method=='POST':
        form=BillingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
    else:
        form=BillingForm()
    return render(request,'billing_form.html',context={'form':form})

@login_required
def billing_update(request, pk):
    billing = get_object_or_404(Billing, pk=pk)
    if request.method == 'POST':
        form=BillingForm(request.POST, instance=billing)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
    else:
        form=BillingForm(instance=billing)
    return render(request,'billing_update.html',{'form':form, 'billing':billing})

@login_required
def billing_delete(request,pk):
    billing = get_object_or_404(Billing, pk=pk)

    if request.method == 'POST':
        billing.delete()
        return redirect('billing_list')

    return render(request,'billing_delete.html',{'billing':billing})
@login_required
def billing_list(request):
    billings = Billing.objects.all().order_by('-billing_date')
    return render(request,'billing_list.html',context={'billings':billings})

@login_required
def patient_medicine(request, pk):
    patient=get_object_or_404(Patient, pk=pk)
    if request.method=='POST':
        form=PatientMedicineForm(request.POST)
        if form.is_valid():
            medicine=form.save(commit=False)
            medicine.patient=patient
            medicine.unit_price=medicine.drug.price
            medicine.save()

            if medicine.quantity > medicine.drug.quantity:
                messages.error(request,'Insufficient Quantity')
            else:
                medicine.drug.quantity -= medicine.quantity
                medicine.drug.save()
                medicine.save()
                messages.success(request,'Medicine Distributed')
                return redirect('patient_medicine_list', pk=patient.pk)
    else:
        form=PatientMedicineForm()
    return render(request,'patient_medicine_form.html',{'form':form,'patient':patient})

@login_required
def patient_medicine_update(request, pk):
    medicine = get_object_or_404(PatientMedicine, pk=pk)
    if request.method == "POST":
        form = PatientMedicineForm(request.POST or None,instance=medicine)

        form.fields['drug'].disabled = True

        if form.is_valid():
            updated=form.save(commit=False)
            medicine.drug.quantity += medicine.quantity

            if updated.quantity>medicine.drug.quantity:
                messages.error(request,'Insufficient Quantity')
            else:
                medicine.drug.quantity -= updated.quantity
                medicine.drug.save()
                updated.unit_price=medicine.drug.price
                updated.save()
                messages.success(request, "Medicine Updated")
                return redirect('patient_medicine_list',pk=medicine.patient.pk)
    else:
        form=PatientMedicineForm(instance=medicine)
        form.fields['drug'].disabled = True
    return render(request,'patient_medicine_form.html',{'form': form,'patient':medicine.patient})

@login_required
def patient_medicine_delete(request, pk):
    medicine = get_object_or_404(PatientMedicine, pk=pk)

    if request.method == "POST":
        patient_pk=medicine.patient.pk
        medicine.delete()
        messages.success(request, "Medicine Deleted")
        return redirect('patient_medicine_list', pk=patient_pk)

    return render(request,'patient_medicine_delete.html',{'medicine': medicine})

@login_required
def patient_medicine_list(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    medicines = PatientMedicine.objects.filter(patient=patient).select_related('drug')
    grand_total = sum(medicine.medicine_total() for medicine in medicines)

    return render(request,'patient_medicine_list.html',{'patient':patient,'medicines': medicines,'grand_total':grand_total})

@login_required
def invoice_detail(request, pk):
    billing = get_object_or_404(Billing, pk=pk)

    invoice, created = Invoice.objects.get_or_create(billing=billing)

    return render(request, 'invoice_detail.html', {'billing': billing,'invoice': invoice,})
