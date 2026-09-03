import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .models import Enquiry


def home(request):
    return render(request, 'index.html')


def details(request):
    return render(request, 'details.html')


@require_POST
def create_enquiry(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = request.POST

    # Honeypot field for simple bot protection.
    if str(data.get('website', '')).strip():
        return JsonResponse({'ok': True, 'message': 'Thank you. Your enquiry has been received.'})

    name = str(data.get('name', '')).strip()
    company = str(data.get('company', '')).strip()
    email = str(data.get('email', '')).strip()
    mobile = str(data.get('mobile', '')).strip()
    service = str(data.get('service', '')).strip()
    message = str(data.get('message', '')).strip()

    if not name or not email or not service:
        return JsonResponse({'ok': False, 'message': 'Please complete your name, email and service.'}, status=400)

    enquiry = Enquiry.objects.create(
        name=name,
        company=company,
        email=email,
        mobile=mobile,
        service=service,
        message=message,
    )

    subject = f'New Infosis Website Enquiry — {service}'
    body = (
        f'New enquiry received from the Infosis website.\n\n'
        f'Name: {name}\n'
        f'Company: {company or "Not provided"}\n'
        f'Email: {email}\n'
        f'Mobile: {mobile or "Not provided"}\n'
        f'Service: {service}\n\n'
        f'Message:\n{message or "Not provided"}\n\n'
        f'Enquiry ID: #{enquiry.pk}'
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ENQUIRY_NOTIFICATION_EMAIL], fail_silently=True)
    except Exception:
        pass

    return JsonResponse({
        'ok': True,
        'message': 'Thank you. Your enquiry has been received. Our team will contact you soon.',
        'reference': f'INF-{enquiry.pk:05d}',
    })


@require_http_methods(['GET', 'POST'])
def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid staff login details.')
    return render(request, 'dashboard_login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard_login')
    enquiries = Enquiry.objects.all()
    status_counts = enquiries.values('status').annotate(total=Count('id'))
    counts = {item['status']: item['total'] for item in status_counts}
    context = {
        'enquiries': enquiries[:100],
        'total': enquiries.count(),
        'new_count': counts.get('new', 0),
        'contacted_count': counts.get('contacted', 0),
        'progress_count': counts.get('in_progress', 0),
        'closed_count': counts.get('closed', 0),
    }
    return render(request, 'dashboard.html', context)


@login_required
@require_POST
def update_status(request, pk):
    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')
    enquiry = get_object_or_404(Enquiry, pk=pk)
    status = request.POST.get('status')
    valid = {key for key, _ in Enquiry.STATUS_CHOICES}
    if status in valid:
        enquiry.status = status
        enquiry.save(update_fields=['status', 'updated_at'])
    return redirect('dashboard')


@login_required
@require_POST
def delete_enquiry(request, pk):
    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')
    enquiry = get_object_or_404(Enquiry, pk=pk)
    enquiry.delete()
    return redirect('dashboard')
