from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Deactivated', 'Deactivated'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    # Link to Django's built-in user model (optional)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    doctor_id = models.AutoField(primary_key=True)  # unique ID
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    licence_number = models.CharField(max_length=50, blank=True, null=True)
    doctor_visit_fees = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    profile_image = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # DESC order


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
