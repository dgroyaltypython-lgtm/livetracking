from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employee
from django.http import JsonResponse
from .models import Trip, Stop
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # SUPERUSER gets admin dashboard
            if user.is_superuser or user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_superuser or request.user.role == 'admin':
        return render(request, 'admin_dashboard.html')

    return redirect('employee_dashboard')


def employee_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'employee_dashboard.html')

def update_location(request):
    if request.method == 'POST' and request.user.is_authenticated:
        import json

        try:
            data = json.loads(request.body)

            lat = float(data.get('latitude'))
            lng = float(data.get('longitude'))

            trip = Trip.objects.filter(
                employee=request.user,
                end_time__isnull=True
            ).last()

            print("ACTIVE TRIP:", trip)

            if not trip:
                return JsonResponse({'status': 'NO ACTIVE TRIP'})

            Stop.objects.create(
                trip=trip,
                latitude=lat,
                longitude=lng
            )

            print("STOP SAVED:", lat, lng)

            return JsonResponse({'status': 'SAVED'})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({'status': 'ERROR'})

    return JsonResponse({'status': 'INVALID'})

def start_trip(request):
    print("🔥 START TRIP HIT")

    if request.method == 'POST' and request.user.is_authenticated:
        try:
            # ✅ Try JSON first
            try:
                data = json.loads(request.body)
                lat = data.get('latitude')
                lng = data.get('longitude')
            except:
                # ✅ Fallback to form data
                lat = request.POST.get('latitude')
                lng = request.POST.get('longitude')

            print("DATA:", lat, lng)

            if not lat or not lng:
                return JsonResponse({'status': 'NO DATA'})

            trip = Trip.objects.create(
                employee=request.user,
                start_lat=float(lat),
                start_lng=float(lng)
            )

            print("✅ TRIP CREATED:", trip)

            return JsonResponse({'status': 'started'})

        except Exception as e:
            print("❌ ERROR:", e)
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'invalid'})


def end_trip(request):
    if request.method == 'POST' and request.user.is_authenticated:
        trip = Trip.objects.filter(employee=request.user, end_time__isnull=True).last()

        if trip:
            trip.end_time = timezone.now()
            trip.end_lat = request.POST.get('latitude')
            trip.end_lng = request.POST.get('longitude')
            trip.save()

        return JsonResponse({'status': 'trip ended'})
    
def get_live_data(request):
    print("USER:", request.user, "AUTH:", request.user.is_authenticated)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})

    # REMOVE role restriction temporarily
    trips = Trip.objects.filter(end_time__isnull=True).prefetch_related('stops')

    data = []

    for trip in trips:
        stops = trip.stops.all().order_by('timestamp')

        path = [
            {"lat": stop.latitude, "lng": stop.longitude}
            for stop in stops
        ]

        if path:
            current_location = path[-1]
        else:
            current_location = {
                "lat": trip.start_lat,
                "lng": trip.start_lng
            }

        data.append({
            "employee": trip.employee.username,
            "current_location": current_location,
            "path": path
        })

    print("DATA SENT:", data)
    return JsonResponse(data, safe=False)   