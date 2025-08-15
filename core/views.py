from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import CustomLoginForm
from .forms import DoctorForm
from .models import Doctor


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    # Get statistics
    # total_patients = Patient.objects.count()
    # total_doctors = Doctor.objects.count()
    # total_appointments = Appointment.objects.count()
    # today_appointments = Appointment.objects.filter(
    # appointment_date=timezone.now().date()    ).count()
    #
    # # Recent appointments
    # recent_appointments = Appointment.objects.select_related(
    #     'patient', 'doctor__user'
    # ).order_by('-created_at')[:5]
    #
    # context = {
    #     'total_patients': total_patients,
    #     'total_doctors': total_doctors,
    #     'total_appointments': total_appointments,
    #     'today_appointments': today_appointments,
    #     'recent_appointments': recent_appointments,
    # }
    return render(request, 'clinic/dashboard.html')

#
# @login_required
# def patient_list(request):
#     query = request.GET.get('q')
#     patients = Patient.objects.all()
#
#     if query:
#         patients = patients.filter(
#             Q(first_name__icontains=query) |
#             Q(last_name__icontains=query) |
#             Q(email__icontains=query) |
#             Q(phone__icontains=query)
#         )
#
#     paginator = Paginator(patients, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'clinic/patient_list.html', {'page_obj': page_obj, 'query': query})


#
#
# @login_required
# def appointment_list(request):
#     appointments = Appointment.objects.select_related(
#         'patient', 'doctor__user'
#     ).order_by('-appointment_date', '-appointment_time')
#
#     paginator = Paginator(appointments, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'clinic/appointment_list.html', {'page_obj': page_obj})




def calendar_view(request):
    return render(request, 'clinic/calendar.html')

def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialization = request.POST.get('specialization')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        dob = request.POST.get('dob') or None
        gender = request.POST.get('gender')
        experience = request.POST.get('experience') or None
        licence_number = request.POST.get('licence_number')
        doctor_visit_fees = request.POST.get('doctor_visit_fees')
        status = request.POST.get('status')
        profile_image = request.FILES.get('profile_image')

        Doctor.objects.create(
            first_name=first_name,
            last_name=last_name,
            specialization=specialization,
            mobile_number=mobile_number,
            email=email,
            address=address,
            dob=dob,
            gender=gender,
            experience=experience,
            licence_number=licence_number,
            doctor_visit_fees=doctor_visit_fees,
            status=status,
            profile_image=profile_image
        )

        messages.success(request, 'Doctor added successfully!')
        return redirect('doctor_list')  # Change to your list page

    context = {
        "status_choices": Doctor.STATUS_CHOICES,
        "gender_choices": Doctor.GENDER_CHOICES,
    }
    return render(request, 'clinic/create_doctor.html', context)


def doctor_list(request):
    query = request.GET.get('q', '')
    doctors = Doctor.objects.all().order_by('-created_at')  # Descending order

    if query:
        doctors = doctors.filter(
            first_name__icontains=query
        ) | doctors.filter(
            last_name__icontains=query
        ) | doctors.filter(
            specialization__icontains=query
        ) | doctors.filter(
            mobile_number__icontains=query
        )

    paginator = Paginator(doctors, 10)  # 10 doctors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'doctors': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'clinic/doctor_list.html', context)



# Add Doctor
def doctor_add(request):
    if request.method == 'POST':
        data = request.POST
        file = request.FILES.get('profile_image')
        doctor = Doctor.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            specialization=data.get('specialization'),
            mobile_number=data.get('mobile_number'),
            email=data.get('email'),
            address=data.get('address'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            experience=data.get('experience'),
            licence_number=data.get('licence_number'),
            doctor_visit_fees=data.get('doctor_visit_fees'),
            status=data.get('status'),
            profile_image=file
        )
        messages.success(request, 'Doctor added successfully!')
        return redirect('doctor_list')
    return render(request, 'clinic/create_doctor.html')
def doctor_edit(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)

    if request.method == "POST":
        doctor.first_name = request.POST.get('first_name', '')
        doctor.last_name = request.POST.get('last_name', '')
        doctor.specialization = request.POST.get('specialization', '')
        doctor.mobile_number = request.POST.get('mobile_number', '')
        doctor.email = request.POST.get('email', '')
        doctor.address = request.POST.get('address', '')
        doctor.gender = request.POST.get('gender', '')
        doctor.experience = request.POST.get('experience') or 0
        doctor.licence_number = request.POST.get('licence_number', '')
        doctor.doctor_visit_fees = request.POST.get('doctor_visit_fees') or 0
        doctor.status = request.POST.get('status', '')

        # Handle date safely
        dob = request.POST.get('dob')
        doctor.dob = dob if dob else None

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            doctor.profile_image = request.FILES['profile_image']

        doctor.save()
        messages.success(request, f'Doctor {doctor.first_name} updated successfully.')
        return redirect('doctor_list')

    context = {
        'doctor': doctor
    }
    return render(request, 'clinic/doctor_edit.html', context)

# Delete Doctor
def doctor_delete(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully!')
    return redirect('doctor_list')

def doctor_details(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    return render(request, 'clinic/doctor_details.html', {'doctor': doctor})