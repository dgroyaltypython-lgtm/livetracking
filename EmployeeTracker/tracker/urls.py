from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('update-location/', views.update_location, name='update_location'),
    path('start-trip/', views.start_trip, name='start_trip'),
    path('end-trip/', views.end_trip, name='end_trip'),
    path('get-live-data/', views.get_live_data, name='get_live_data'),
]