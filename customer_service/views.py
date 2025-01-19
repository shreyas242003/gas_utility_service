from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ServiceRequest
from .forms import ServiceRequestForm, UpdateRequestForm
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache





@login_required
@user_passes_test(lambda u: u.is_staff)  
def support_dashboard(request):
    requests = ServiceRequest.objects.all()
    return render(request, 'support/dashboard.html', {'requests': requests})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
           
            user.is_staff = False
            user.save()
            return redirect('login')  
    else:
        form = UserCreationForm()

    return render(request, 'customer_service/register.html', {'form': form})
# View to Submit a Service Request
RATE_LIMIT_TIME = 60  
RATE_LIMIT_KEY_PREFIX = "rate_limit:"

@login_required
def submit_request(request):
    if request.method == 'POST':
        # Check if the user has submitted a request recently
        last_submission_time = cache.get(RATE_LIMIT_KEY_PREFIX + str(request.user.id))

        if last_submission_time:
            time_diff = timezone.now() - last_submission_time
            if time_diff < timezone.timedelta(seconds=RATE_LIMIT_TIME):
                # If the difference is less than the rate limit time, reject the request
                return render(request, 'customer_service/submit_request.html', {
                    'form': ServiceRequestForm(),
                    'error_message': 'You are submitting requests too quickly. Please wait a moment and try again.'
                })
     
       
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  
            service_request.save()

            cache.set(RATE_LIMIT_KEY_PREFIX + str(request.user.id), timezone.now(), timeout=RATE_LIMIT_TIME)

            return redirect('request_status')  
    else:
        form = ServiceRequestForm()

    return render(request, 'customer_service/submit_request.html', {'form': form})

@login_required
def request_status(request):
    service_requests = ServiceRequest.objects.filter(user=request.user)  # Fetch only the logged-in user's requests
    return render(request, 'customer_service/request_status.html', {'service_requests': service_requests})


@login_required
@user_passes_test(lambda u: u.is_staff)
def update_request_status(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if request.method == 'POST':
        form = UpdateRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            service_request = form.save(commit=False)
            if service_request.status == ServiceRequest.COMPLETED and not service_request.resolved_at:
                service_request.resolved_at = timezone.now()
            service_request.save()
            
            return redirect('support_dashboard')
    else:
        form = UpdateRequestForm(instance=service_request)

    return render(request, 'support/update_request.html', {'form': form, 'service_request': service_request})


@login_required  
def account_info(request):
    if not request.user.is_staff:
        user = request.user
        service_requests = ServiceRequest.objects.filter(user=user)
        pending_requests_count = service_requests.filter(status='Pending').count()
        return render(request, 'support/account_info.html', {
            'user': user,
            'service_requests': service_requests,
            'pending_requests_count': pending_requests_count,
        })
    return HttpResponse("Unauthorized", status=403)


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('support_dashboard')
        else:
            return redirect('submit_request')
    return render(request, 'customer_service/home.html')
