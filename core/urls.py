from django.urls import path
from . import views
from .views import calendar_view

urlpatterns = [
    path('', views.custom_login, name='login'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('patients/list', views.patient_list, name='patient_list'),
    # path('patients/add/', views.patient_create, name='patient_create'),
    # path('appointments/', views.appointment_list, name='appointment_list'),
    # path('appointments/add/', views.appointment_create, name='appointment_create'),
    path('doctors/list', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='doctor_create'),

    path('calendar/', calendar_view, name='calendar'),

path('doctors/edit/<int:doctor_id>/', views.doctor_edit, name='doctor_edit'),
    path('doctors/delete/<int:doctor_id>/', views.doctor_delete, name='doctor_delete'),
    path('doctors/details/<int:doctor_id>/', views.doctor_details, name='doctor_details'),

]